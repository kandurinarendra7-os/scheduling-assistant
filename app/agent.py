def booking_specialist(state: AgentState):
    """Manages calendar tool execution and prompts for missing info."""
    messages = state["messages"]
    
    # We use 4 curly braces to escape properly for both Python f-strings and LangChain
    system_message = (
        f"You are a Booking Specialist. The current date is {datetime.date.today()}. "
        "Extract the requested date, time, and email from the conversation. If missing, ask the user for them. "
        "Respond ONLY in JSON format: {{{{ \"date\": \"YYYY-MM-DD or relative like 'tomorrow'\", \"time\": \"HH:MM\", \"email\": \"user@example.com\", \"message\": \"Message to user\" }}}}. "
        "If you have all info, set message to 'READY'."
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
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
            
    except Exception as e:
        print(f"Error in booking specialist: {e}")
        return {"messages": [AIMessage(content="I'm having trouble processing that. Could you please provide the date, time, and your email address?")]}
