# Multi-Agent Scheduling Assistant

A sophisticated scheduling application built with **LangGraph**, **Streamlit**, and **OpenAI** that orchestrates multiple AI agents to handle calendar bookings and appointment management.
HAVE A LOOK AT MY PROJECT:https://scheduling-assistant-jfewropyhidzvkrmrfxmwd.streamlit.app/

## 📋 Overview

This project implements a multi-agent workflow that combines:

- **Triage Agent**: Analyzes incoming user messages and determines intent (general query vs. booking request)
- **Booking Specialist**: Manages calendar operations, validates dates/times, and handles appointment reservations
- **Tool Suite**: Mock calendar tools for checking availability, reserving slots, and sending notifications
- **Persistent State**: SQLite-backed conversation history that survives page refreshes

## ✨ Key Features

### 1. Agent Architecture
- **LangGraph-based state machine** for intelligent routing between agents
- **Triage Agent** classifies user intent and routes appropriately
- **Booking Specialist** handles complex scheduling logic with error recovery

### 2. Input Normalization & Validation
- Converts relative dates ("tomorrow", "today") to YYYY-MM-DD format
- Validates time formats (HH:MM)
- Email validation for booking confirmations

### 3. Negotiation & Error Handling
- When a requested slot is unavailable, the agent suggests alternatives
- Graceful error handling with user-friendly messages
- Prompts for missing information before proceeding

### 4. Mock Tools (Fully Functional)
- `check_availability(date)`: Returns available time slots for a given date
- `reserve_slot(date, time, email)`: Reserves an appointment slot
- `send_booking_notification(email, details)`: Simulates notification delivery

### 5. State Persistence
- SQLite-based memory store for conversation history
- Thread-based conversation tracking
- Survives page refreshes and browser restarts

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd scheduling_assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

4. **Run the Streamlit app**
   ```bash
   streamlit run streamlit_app.py
   ```

The app will open at `http://localhost:8501`

## 📁 Project Structure

```
scheduling_assistant/
├── app/
│   ├── __init__.py
│   ├── agent.py           # LangGraph agents and workflow
│   ├── tools.py           # Mock calendar tools
│   └── app.py             # Legacy Streamlit integration
├── data/                  # Data storage directory
├── streamlit_app.py       # Main Streamlit entry point
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── .env.example           # Example environment file
└── README.md              # This file
```

## 🔧 Architecture

### State Management
```
AgentState = {
    messages: List[BaseMessage]  # Conversation history
    intent: str                  # BOOKING or GENERAL
    date: str                    # YYYY-MM-DD format
    time: str                    # HH:MM format
    email: str                   # User email
    booking_status: str          # SUCCESS or FAILED
}
```

### Agent Flow
```
User Input
    ↓
[Triage Agent]
    ├─→ GENERAL → [Response] → END
    └─→ BOOKING → [Booking Specialist]
                      ├─→ Extract Details
                      ├─→ Validate Date/Time
                      ├─→ Check Availability
                      ├─→ Reserve Slot
                      └─→ Send Notification → END
```

## 💬 Usage Examples

### Example 1: General Query
**User**: "What are your business hours?"
**Agent**: Responds directly as Triage Agent (GENERAL intent)

### Example 2: Book an Appointment
**User**: "I'd like to book an appointment for tomorrow at 10:00 AM"
**Agent**: 
1. Triage Agent detects BOOKING intent
2. Booking Specialist extracts date (tomorrow → 2026-07-15), time (10:00), and requests email
3. Validates availability
4. Reserves slot
5. Sends confirmation notification

### Example 3: Negotiation
**User**: "Can I book tomorrow at 11:00?"
**Agent**: "That slot is unavailable. Available times are: 10:00, 14:00. Which would you prefer?"

## 🛠️ Configuration

### Mock Database
Edit `app/tools.py` to modify available slots:
```python
mock_db = {
    "2026-07-15": {
        "10:00": None,      # Available
        "11:00": "booked",  # Booked
        "14:00": None,
    },
}
```

### LLM Model
Change the model in `app/agent.py`:
```python
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
```

## 🔐 Environment Variables

Create a `.env` file:
```
OPENAI_API_KEY=sk-your-key-here
```

## 📦 Deployment

### Streamlit Cloud
1. Push to GitHub
2. Connect repository to Streamlit Cloud
3. Deploy with automatic secret management

### Render
1. Create a new Render service
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `streamlit run streamlit_app.py`

### Hugging Face Spaces
1. Create a new Space
2. Upload files
3. Set runtime to Streamlit
4. Add secrets for OPENAI_API_KEY

## 🧪 Testing

### Test Triage Agent
```
User: "What's the weather?"
Expected: GENERAL response
```

### Test Booking Specialist
```
User: "Book me tomorrow at 10:00, my email is test@example.com"
Expected: Confirmation message with booking details
```

### Test Error Handling
```
User: "Book tomorrow at 11:00"
Expected: Slot unavailable message with alternatives
```

## 📝 Notes

- The mock database is in-memory; data persists only during the session
- For production, replace mock tools with real calendar APIs (Google Calendar, Calendly, etc.)
- Conversation history uses SQLite; can be upgraded to persistent database
- The app uses `gpt-4o-mini` for cost efficiency; upgrade to `gpt-4` for better reasoning

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Troubleshooting

### "OPENAI_API_KEY not found"
- Ensure `.env` file exists in the project root
- Verify the key is set correctly
- Restart the Streamlit app

### "Module not found" errors
- Run `pip install -r requirements.txt`
- Ensure you're in the correct virtual environment

### Slots not reserving
- Check `app/tools.py` for mock database configuration
- Verify date format is YYYY-MM-DD

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

Built with ❤️ using LangGraph and Streamlit
