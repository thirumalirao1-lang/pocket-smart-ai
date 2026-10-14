from flask import Blueprint
from config import Config
from services.gemini_service import GeminiService

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def health():
    gemini = GeminiService()
    return {
        "success": True,
        "status": "ok",
        "ai_configured": gemini.is_configured(),
        "model": Config.GEMINI_MODEL,
        "mock_mode": Config.USE_MOCK_AI,
    }
