# backend/app/services/appointment_tools.py

# --------------------------------------------
# MOCK DATABASES (you can replace with real DB later)
# --------------------------------------------

DOCTOR_SLOTS = {
    "1": {
        "2025-02-01": ["9:00 AM", "11:00 AM", "2:00 PM"],
        "2025-02-02": ["10:00 AM", "1:00 PM"],
    },
    "2": {
        "2025-02-01": ["10:30 AM", "3:30 PM"],
        "2025-02-03": ["9:00 AM"],
    },
}

APPOINTMENTS = []


# --------------------------------------------
# 1️⃣ CHECK AVAILABILITY
# --------------------------------------------
def check_availability(doctor_id: str, date: str):
    slots = DOCTOR_SLOTS.get(doctor_id, {}).get(date, [])
    return {
        "doctor_id": doctor_id,
        "date": date,
        "available_slots": slots
    }


# --------------------------------------------
# 2️⃣ CREATE APPOINTMENT
# --------------------------------------------
def create_appointment(doctor_id: str, patient_id: str, date: str, slot: str):
    appointment = {
        "doctor_id": doctor_id,
        "patient_id": patient_id,
        "date": date,
        "slot": slot
    }

    APPOINTMENTS.append(appointment)

    return {
        "status": "success",
        "appointment": appointment
    }


# --------------------------------------------
# 3️⃣ SEND EMAIL (MOCK FUNCTION)
# --------------------------------------------
def send_email(to: str, subject: str, body: str):
    # (In real system you'd integrate Gmail API)
    return {
        "status": "sent",
        "to": to,
        "subject": subject,
        "body": body
    }
