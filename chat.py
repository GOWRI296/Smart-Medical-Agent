from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm_agent import run_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session: dict | None = None

@router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        reply_dict, updated_session = run_agent(req.message, req.session)

        # reply_dict MUST contain {"message": "..."}
        message_text = reply_dict.get("message", "")

        # RETURN EXACT SHAPE FRONTEND EXPECTS
        return {
            "message": message_text,
            "session": updated_session
        }

    except Exception as e:
        print("CHAT ERROR:", e)
        return {
            "message": f"⚠️ Server error: {str(e)}",
            "session": req.session or {}
        }
