# app/services/doctor_tools.py

def doctor_stats(query: str):
    query = query.lower()

    if "yesterday" in query:
        return "Yesterday 12 patients visited."

    if "today" in query:
        return "You have 8 appointments today."

    if "tomorrow" in query:
        return "You have 5 appointments tomorrow."

    if "fever" in query:
        return "5 patients reported fever this week."

    return "No matching statistical data found."
