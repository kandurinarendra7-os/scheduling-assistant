import os
from typing import TypedDict, Annotated, Sequence, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.tools import check_availability, reserve_slot, send_booking_notification, resolve_date
import datetime
import json
import streamlit as st

# --- Initialize LLM with Groq (FREE TIER) ---
# We use llama-3.3-70b-versatile because it is highly capable and free on Groq
def get_llm():
    # Try to get API key from Streamlit secrets first, then environment variables
    groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=groq_api_key
    )

llm = get_llm()

# Define the state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    intent: str
    date: str
    time: str
    email: str
    booking_status: str

# --- Nodes ---

def triage_agent(state: AgentState):
    """Analyzes incoming user messages and routes them."""
    messages = state["messages"]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Triage Agent. Your job is to determine if the user wants to schedule, check, or book an appointment. If they do, respond with 'INTENT: BOOKING'. If it's a general query, respond with a helpful answer and 'INTENT: GENERAL'."),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"messages": messages})
    
    content = response.content
    intent = "GENERAL"
    if "INTENT: BOOKING" in content:
        intent = "BOOKING"
        content = content.replace("INTENT: BOOKING", "").strip()
    elif "INTENT: GENERAL" in content:
        intent = "GENERAL"
        content = content.replace("INTENT: GENERAL", "").strip()
        
    return {"messages": [AIMessage(content=content)], "intent": intent}

def booking_specialist(state: AgentState):
    """Manages calendar tool execution and prompts for missing info."""
    messages = state["messages"]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are a Booking Specialist. The current date is {datetime.date.today()}. Extract the requested date, time, and email from the conversation. If missing, ask the user for them. Respond ONLY in JSON format: {{\"date\": \"YYYY-MM-DD or relative like 'tomorrow'\", \"time\": \"HH:MM\", \"email\": \"user@example.com\", \"message\": \"Message to user\"}}. If you have all info, set message to 'READY'."),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"messages": messages})
    
    try:
        content = response.content
        # Robust JSON extraction
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip()
            
        data = json.loads(content)
        date = data.get("date", "")
        time = data.get("time", "")
        email = data.get("email", "")
        message = data.get("message", "")
        
        if message != "READY":
            return {"messages": [AIMessage(content=message)], "date": date, "time": time, "email": email}
            
        resolved_date = resolve_date(date)
        if resolved_date == "Invalid Date":
            return {"messages": [AIMessage(content="I couldn't understand the date. Please provide a valid date (e.g., YYYY-MM-DD or 'tomorrow').")]}
            
        availability = check_availability(resolved_date)
        if not availability:
            return {"messages": [AIMessage(content=f"I'm sorry, but there are no slots available on {resolved_date}. Would you like to try another date?")]}
            
        if time not in availability or availability[time] is not None:
            available_slots = [t for t, status in availability.items() if status is None]
            slots_str = ", ".join(available_slots) if available_slots else "None"
            return {"messages": [AIMessage(content=f"The requested time {time} is not available on {resolved_date}. Available slots are: {slots_str}. Please choose one.")]}
            
        success = reserve_slot(resolved_date, time, email)
        if success:
            send_booking_notification(email, f"Appointment booked for {resolved_date} at {time}.")
            return {"messages": [AIMessage(content=f"Great! Your appointment is booked for {resolved_date} at {time}. A confirmation has been sent to {email}.")], "booking_status": "SUCCESS"}
        else:
            return {"messages": [AIMessage(content="There was an error booking your appointment. Please try again.")], "booking_status": "FAILED"}
            
    except Exception:
        return {"messages": [AIMessage(content="I'm having trouble processing that. Could you please provide the date, time, and your email address?")]}

# --- Routing ---

def route_triage(state: AgentState) -> Literal["booking_specialist", "__end__"]:
    if state.get("intent") == "BOOKING":
        return "booking_specialist"
    return "__end__"

# --- Build Graph ---

workflow = StateGraph(AgentState)
workflow.add_node("triage_agent", triage_agent)
workflow.add_node("booking_specialist", booking_specialist)
workflow.set_entry_point("triage_agent")
workflow.add_conditional_edges("triage_agent", route_triage)
workflow.add_edge("booking_specialist", END)
