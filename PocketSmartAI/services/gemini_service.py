import json
from typing import Any, Dict, Optional
from config import Config

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

class GeminiService:
    def __init__(self):
        self.client = None
        if genai is not None and Config.GEMINI_API_KEY:
            self.client = genai.Client(api_key=Config.GEMINI_API_KEY)

    def is_configured(self) -> bool:
        return self.client is not None and not Config.USE_MOCK_AI

    def generate_json(
        self,
        prompt: str,
        image_bytes: Optional[bytes] = None,
        mime_type: Optional[str] = None
    ) -> Dict[str, Any]:
        if not self.is_configured():
            raise RuntimeError("Gemini AI is not configured")

        contents = [prompt]
        if image_bytes:
            contents.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type or "image/jpeg"
                )
            )

        response = self.client.models.generate_content(
            model=Config.GEMINI_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.35,
                max_output_tokens=4096,
                response_mime_type="application/json",
            ),
        )

        raw = (response.text or "").strip()
        cleaned = raw.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Gemini returned invalid JSON") from exc
