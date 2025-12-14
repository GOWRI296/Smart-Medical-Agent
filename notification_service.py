# backend/app/services/notification_service.py

def send_notification(doctor_id: str, message: str):
    """
    Mock notification service.
    Prints a simulated Slack/WhatsApp message.
    """

    print("\n--- NOTIFICATION SENT ---")
    print(f"Doctor ID: {doctor_id}")
    print(f"Message:\n{message}")
    print("-------------------------\n")

    return {"status": "sent"}
