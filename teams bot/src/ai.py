from datetime import datetime as dt
from os import getenv

from dotenv import load_dotenv
from log import get_logger
from requests import post

load_dotenv()

logger = get_logger(__name__)


PEOPLE_COACH_AI_API_KEY = getenv("PEOPLECOACH_AI_API_KEY", "")
PEOPLE_COACH_AI_BASE_URL = getenv("PEOPLECOACH_AI_CHAT_ENDPOINT", "")
PEOPLE_COACH_AI_CHAT_URL = PEOPLE_COACH_AI_BASE_URL + "/chat"
PEOPLE_COACH_AI_FEEDBACK_URL = PEOPLE_COACH_AI_BASE_URL + "/message_feedback"


def get_people_coach_chat_body(query: str) -> dict:
    return {
        "text": query,
        "user_id": "jitendrakushwah@bitcot.com",
        "timestamp": str(dt.now()),
        "is_teams_chat": True,
        "is_related_question": False,
    }


def get_people_coach_ai_headers() -> dict[str, str]:
    return {"x-api-key": PEOPLE_COACH_AI_API_KEY}


def get_people_coach_ai_response(query: str) -> dict | None:
    """Returns dict with text, message_id, conversation_id or None on failure."""
    try:
        response = post(
            url=PEOPLE_COACH_AI_CHAT_URL,
            json=get_people_coach_chat_body(query=query),
            headers=get_people_coach_ai_headers(),
            timeout=130,
        )
        if response.status_code == 200:
            data = response.json()["response"]
            return {
                "text": data["message"]["text"],
                "message_id": data.get("message_id", ""),
                "conversation_id": data.get("conversation_id", ""),
            }
        logger.error(f"Chat API returned {response.status_code}")
        return None
    except Exception as exc:
        logger.error(f"Chat API request failed: {exc}")
        return None


def post_message_feedback(
    conversation_id: str,
    message_id: str,
    positive: bool,
    reason: str,
    user_id: str = "jitendrakushwah@bitcot.com",
) -> None:
    payload = {
        "conversation_id": conversation_id,
        "feedback_time": dt.now().isoformat(),
        "message_id": message_id,
        "positive": positive,
        "reason": reason,
        "user_id": user_id,
    }
    try:
        response = post(
            url=PEOPLE_COACH_AI_FEEDBACK_URL,
            json=payload,
            timeout=30,
            headers=get_people_coach_ai_headers(),
        )
        if response.status_code != 201:
            logger.error(f"Feedback API returned {response.status_code}")
        else:
            logger.info(f"Feedback posted: positive={positive} message_id={message_id}")
    except Exception as exc:
        logger.error(f"Feedback API request failed: {exc}")
