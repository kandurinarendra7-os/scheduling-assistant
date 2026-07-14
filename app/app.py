
import streamlit as st
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from app.agent import AgentState, triage_agent, booking_specialist, route_triage, workflow
import os

# Set up LangGraph memory
memory = SqliteSaver.from_conn_string(":memory:")

# Compile the workflow with memory
app = workflow.compile(checkpointer=memory)

st.set_page_config(page_title="Scheduling Assistant", page_icon=":calendar:")
st.title("Multi-Agent Scheduling Assistant")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [AIMessage(content="Hello! How can I help you today?")]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# React to user input
if prompt := st.chat_input("What do you want to do?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append(HumanMessage(content=prompt))

    # Invoke the agent
    config = {"configurable": {"thread_id": "1"}} # Using a fixed thread_id for simplicity
    
    # Prepare the input for the agent
    # The agent expects a list of messages, so we pass the current chat history
    input_messages = {"messages": st.session_state.messages}
    
    # Run the agent
    response = app.invoke(input_messages, config=config)
    
    # Extract the last message from the agent's response
    ai_message = response["messages"][-1]
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(ai_message.content)
    # Add assistant response to chat history
    st.session_state.messages.append(ai_message)

