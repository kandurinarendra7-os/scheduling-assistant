import streamlit as st
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage, AIMessage
from app.agent import workflow
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up LangGraph memory
memory = SqliteSaver.from_conn_string(":memory:")

# Compile the workflow with memory
app = workflow.compile(checkpointer=memory)

st.set_page_config(page_title="Scheduling Assistant", page_icon=":calendar:", layout="wide")

# Sidebar
with st.sidebar:
    st.header("About")
    st.write("""
    This is a Multi-Agent Scheduling Assistant powered by LangGraph and Streamlit.
    
    **Features:**
    - Triage Agent: Analyzes your intent
    - Booking Specialist: Manages appointments
    - Persistent state management
    - Mock notification system
    """)

st.title("📅 Multi-Agent Scheduling Assistant")
st.markdown("---")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [AIMessage(content="Hello! I'm your scheduling assistant. How can I help you today? You can ask me to:\n\n- **Check availability** for a specific date\n- **Book an appointment** with your preferred date and time\n- **Answer general questions** about scheduling")]

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = "1"

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user", avatar="👤"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(message.content)

# React to user input
if prompt := st.chat_input("Type your message here..."):
    # Display user message in chat message container
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append(HumanMessage(content=prompt))

    # Invoke the agent
    config = {"configurable": {"thread_id": st.session_state["thread_id"]}}
    
    # Prepare the input for the agent
    input_messages = {"messages": st.session_state.messages}
    
    # Run the agent with spinner
    with st.spinner("Processing..."):
        try:
            response = app.invoke(input_messages, config=config)
            
            # Extract the last message from the agent's response
            ai_message = response["messages"][-1]
            
            # Display assistant response in chat message container
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(ai_message.content)
            # Add assistant response to chat history
            st.session_state.messages.append(ai_message)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please ensure your OPENAI_API_KEY is set correctly in the .env file.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using LangGraph and Streamlit")
