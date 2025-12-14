# backend/app/services/email_service.py

def send_email(to: str, subject: str, body: str):
    """
    Mock email sender — no real SMTP.
    """
    print("\n--- EMAIL SENT ---")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"Body:\n{body}")
    print("------------------\n")

    return {"status": "success"}
