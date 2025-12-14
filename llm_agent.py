import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI

# Import your tools
from app.services.doctor_tools import doctor_stats
from app.services.appointment_tools import (
    check_availability,
    create_appointment,
    send_email
)
from app.services.calendar_tools import create_calendar_event

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -----------------------------
# SAFE HELPERS
# -----------------------------
def safe_json(raw):
    try:
        return json.loads(raw)
    except:
        return {}


def ensure_text(value):
    """Ensures ALL backend output is plain string (frontend-safe)."""
    if isinstance(value, (dict, list)):
        return json.dumps(value, indent=2)
    return str(value)


# -----------------------------
# MAIN AGENT FUNCTION
# -----------------------------
def run_agent(prompt: str, session_context=None):

    if session_context is None:
        session_context = {}

    last_context = session_context.get("last_message", "")

    # =============================================================
    # 🔥 DIRECT BOOKING DETECTOR (Before LLM)
    # =============================================================
    pattern = r"(book|schedule|appointment).*doctor\s+(\d+).*patient\s+(\d+).*on\s+(\d{4}-\d{2}-\d{2}).*(\d{1,2}:\d{2}\s*(AM|PM))"
    match = re.search(pattern, prompt, re.IGNORECASE)

    if match:
        doctor_id = match.group(2)
        patient_id = match.group(3)
        date = match.group(4)
        slot = match.group(5)

        result = create_appointment(doctor_id, patient_id, date, slot)

        reply = (
            "✅ **Appointment Booked (Direct Mode)**\n\n"
            f"👨‍⚕️ Doctor: {doctor_id}\n"
            f"🙍 Patient: {patient_id}\n"
            f"📅 Date: {date}\n"
            f"⏰ Slot: {slot}\n\n"
            f"📤 Confirmation:\n{ensure_text(result)}"
        )

        session_context["last_message"] = reply
        return {"message": ensure_text(reply)}, session_context

    # =============================================================
    # NORMAL LLM CALL
    # =============================================================
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a smart medical assistant that uses tools when necessary."
            },
            {
                "role": "user",
                "content": f"Context: {last_context}\nUser: {prompt}"
            }
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "doctor_stats",
                    "description": "Return doctor visit statistics.",
                    "parameters": {
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_availability",
                    "description": "Check availability for a doctor on a date.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "doctor_id": {"type": "string"},
                            "date": {"type": "string"},
                        },
                        "required": ["doctor_id", "date"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_appointment",
                    "description": "Book an appointment.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "doctor_id": {"type": "string"},
                            "patient_id": {"type": "string"},
                            "date": {"type": "string"},
                            "slot": {"type": "string"},
                        },
                        "required": ["doctor_id", "patient_id", "date", "slot"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "send_email",
                    "description": "Send an email message.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "to": {"type": "string"},
                            "subject": {"type": "string"},
                            "body": {"type": "string"},
                        },
                        "required": ["to", "subject", "body"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_calendar_event",
                    "description": "Create an event in Google Calendar.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "doctor_id": {"type": "string"},
                            "patient_id": {"type": "string"},
                            "date": {"type": "string"},
                            "slot": {"type": "string"},
                        },
                        "required": ["doctor_id", "patient_id", "date", "slot"]
                    }
                }
            }
        ]
    )

    msg = response.choices[0].message

    # =============================================================
    # TOOL CALL HANDLING
    # =============================================================
    if msg.tool_calls:

        tool = msg.tool_calls[0]
        tool_name = tool.function.name
        args = safe_json(tool.function.arguments)

        if tool_name == "doctor_stats":
            result = doctor_stats(args.get("query", ""))
            reply = f"📊 Doctor Stats:\n{ensure_text(result)}"

        elif tool_name == "check_availability":
            result = check_availability(args.get("doctor_id"), args.get("date"))
            reply = f"🗓 Availability:\n{ensure_text(result)}"

        elif tool_name == "create_appointment":
            result = create_appointment(
                args.get("doctor_id"),
                args.get("patient_id"),
                args.get("date"),
                args.get("slot"),
            )
            reply = f"✅ Appointment Created:\n{ensure_text(result)}"

        elif tool_name == "send_email":
            result = send_email(
                args.get("to"),
                args.get("subject"),
                args.get("body"),
            )
            reply = f"📧 Email Sent:\n{ensure_text(result)}"

        elif tool_name == "create_calendar_event":
            result = create_calendar_event(
                args.get("doctor_id"),
                args.get("patient_id"),
                args.get("date"),
                args.get("slot"),
            )
            reply = (
                "📅 Google Calendar Event Created\n"
                f"🔗 Link: {result.get('link')}\n"
                f"🆔 Event: {result.get('event_id')}"
            )

        else:
            reply = "⚠️ Unknown tool requested."

    else:
        reply = ensure_text(msg.content)

    # Save context for multi-turn chat
    session_context["last_message"] = reply

    # 🔥 ALWAYS RETURN EXACTLY TWO VALUES
    return {"message": ensure_text(reply)}, session_context
