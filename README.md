# Smart-Medical-Agent
This project implements an AI-powered medical assistant that can:  Check doctor availability  Book patient appointments  Send confirmation notifications  Generate doctor summary reports  Maintain multi-turn conversation memory  Create Google Calendar events



This project implements an AI-powered medical assistant that can:

Check doctor availability

Book patient appointments

Send confirmation notifications

Generate doctor summary reports

Maintain multi-turn conversation memory

Create Google Calendar events

🚀 How to Run the Project
Backend (FastAPI)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload


Backend starts at:

👉 http://127.0.0.1:8000/chat

Frontend (React)
cd frontend
npm install
npm start


Frontend starts at:

👉 http://localhost:3000/

🧪 Sample Prompts You Can Try
Check availability for doctor 1 on 2025-02-01
Book an appointment with doctor 1 for patient 10 on 2025-02-01 at 9:00 AM
How many patients visited yesterday?
Give me today's appointment summary


📂 Project Structure

You must paste this inside README.md.
NO need to create a separate file.

smart-medical-agent/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   └── chat.py
│   │   ├── services/
│   │   │   ├── llm_agent.py
│   │   │   ├── doctor_tools.py
│   │   │   ├── appointment_tools.py
│   │   │   └── calendar_tools.py
│   ├── requirements.txt
│   └── .env
│
└── frontend/
    ├── src/
    │   ├── Chat.js
    │   └── Chat.css
    ├── public/
    └── package.json

📦 Where to Store This?

👉 Inside README.md only.
Do NOT create a new folder or file for project structure.

Your repo should have:

README.md   ← (put everything here)
backend/
frontend/
