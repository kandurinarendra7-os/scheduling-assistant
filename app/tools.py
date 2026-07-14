
import datetime

# Mock database for availability and bookings
mock_db = {
    "2026-07-15": {
        "10:00": None,  # Available
        "11:00": "booked", # Booked
        "14:00": None,
    },
    "2026-07-16": {
        "09:00": None,
        "10:00": None,
        "15:00": None,
    },
}

def check_availability(date: str) -> dict:
    """Checks availability for a given date. Date format: YYYY-MM-DD."""
    print(f"Checking availability for {date}...")
    return mock_db.get(date, {})

def reserve_slot(date: str, time: str, email: str) -> bool:
    """Reserves a slot for a given date, time, and email. Date format: YYYY-MM-DD, Time format: HH:MM."""
    print(f"Attempting to reserve slot for {email} on {date} at {time}...")
    if date in mock_db and time in mock_db[date] and mock_db[date][time] is None:
        mock_db[date][time] = email
        print(f"Slot {date} {time} reserved for {email}.")
        return True
    print(f"Failed to reserve slot {date} {time}.")
    return False

def send_booking_notification(email: str, details: str) -> bool:
    """Simulates sending a booking confirmation notification."""
    print(f"Sending booking notification to {email} with details: {details}")
    # In a real application, this would interact with a webhook or API
    return True

# Helper function to resolve relative dates
def resolve_date(date_str: str) -> str:
    today = datetime.date.today()
    if date_str.lower() == "tomorrow":
        return (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    elif date_str.lower() == "today":
        return today.strftime("%Y-%m-%d")
    # Add more relative date handling as needed
    try:
        # Assume YYYY-MM-DD format if not relative
        datetime.date.fromisoformat(date_str)
        return date_str
    except ValueError:
        return "Invalid Date"

