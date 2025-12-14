import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google Calendar scope
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():
    """
    Authenticates using credentials.json and returns a Google Calendar service object.
    Saves token.json so login happens only once.
    """
    creds = None

    # If token already exists → load it.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If no valid token → open browser to authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save new token for next time
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)
    return service


def create_calendar_event(summary, start_time, end_time):
    """
    Creates a REAL Google Calendar event.
    start_time and end_time must be ISO format (YYYY-MM-DDTHH:MM:SS)
    """
    try:
        service = get_calendar_service()

        event = {
            "summary": summary,
            "start": {"dateTime": start_time, "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": end_time, "timeZone": "Asia/Kolkata"},
        }

        created_event = service.events().insert(calendarId="primary", body=event).execute()

        return {
            "status": "success",
            "event_id": created_event["id"],
            "html_link": created_event["htmlLink"],
            "message": "Calendar event created successfully!"
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
