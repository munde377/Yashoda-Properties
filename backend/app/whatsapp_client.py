import os
import httpx
from dotenv import load_dotenv

load_dotenv()
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL")
WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY")


def render_template(body: str, variables: dict[str, str]) -> str:
    result = body
    for key, value in variables.items():
        result = result.replace(f"{{{{{key}}}}}", str(value))
    return result


def send_whatsapp_message(phone: str, message: str) -> dict:
    if not WHATSAPP_API_URL or not WHATSAPP_API_KEY:
        return {"success": False, "error": "WhatsApp API configuration is missing."}

    payload = {
        "recipient": phone,
        "message": message,
    }
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = httpx.post(WHATSAPP_API_URL, json=payload, headers=headers, timeout=10.0)
        response.raise_for_status()
        return {"success": True, "payload": response.json()}
    except Exception as exc:
        return {"success": False, "error": str(exc)}
