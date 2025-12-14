# backend/app/services/google_calendar.py

from datetime import datetime, timedelta
import uuid

# Mock Google Calendar Service (NO real API)
# You can upgrade this later.

def check_google_calendar_freebusy(doctor_id: str, date: datetime):
    """
    Returns dummy available slots for a doctor.
    """
    slots = []
    start_hour = 9
    for i in range(3):  # 9-10, 10-11, 11-12
        slots.append({
            "start_time": date.replace(hour=start_hour + i, minute=0, second=0),
            "end_time": date.replace(hour=start_hour + i + 1, minute=0, second=0),
            "is_available": True
        })

    return slots


def create_calendar_event(doctor_id: str, start: datetime, end: datetime, reason: str):
    """
    Creates a dummy event and returns an event ID.
    """
    event_id = f"event-{uuid.uuid4()}"
    return event_id
