import json
from models import PlannerResult, RecommendationItem, clean_number
from services.gemini_service import GeminiService
from services.mock_data import home_mock, party_mock, jewelry_mock

class PlannerService:
    def __init__(self):
        self.ai = GeminiService()

    def home(self, data):
        budget = clean_number(data.get("budget"), "Budget", 1)
        rooms = data.get("rooms", [])
        if not isinstance(rooms, list):
            raise ValueError("Rooms must be a list")
        room_names = []
        for room in rooms:
            if isinstance(room, dict):
                name = str(room.get("name", "")).strip()
                items = room.get("items", [])
                if name:
                    room_names.append(name + (": " + ", ".join(map(str, items)) if items else ""))
            else:
                room_names.append(str(room))

        if not self.ai.is_configured():
            return home_mock(budget, room_names)

        prompt = f"""Create a practical home interior budget plan.
Budget: {budget}
Rooms and requested items: {json.dumps(room_names)}
Return JSON only:
{{
  "allocation": {{"furniture": 0, "decor": 0, "lighting": 0, "storage": 0, "reserve": 0}},
  "recommendations": [{{"name":"","category":"","estimated_price":0,"platform":"","url":"","reason":"","quantity":1}}],
  "notes": []
}}
Allocation total must equal the budget. Use realistic estimates and do not claim live prices."""
        return self._convert_result("Home Interior Planner", budget, self.ai.generate_json(prompt), True)

    def party(self, data):
        budget = clean_number(data.get("budget"), "Budget", 1)
        guests = int(clean_number(data.get("guests"), "Guest count", 1))
        event_type = str(data.get("event_type", "")).strip()
        venue = str(data.get("venue", "")).strip()
        if not event_type:
            raise ValueError("Event type is required")
        if not venue:
            raise ValueError("Venue information is required")

        if not self.ai.is_configured():
            return party_mock(budget, guests, event_type, venue)

        prompt = f"""Create a party budget plan.
Budget: {budget}
Guests: {guests}
Event type: {event_type}
Venue: {venue}
Return JSON only with allocation keys venue, catering, decor, entertainment, venue_stay,
recommendations array and notes array. Allocation total must equal budget."""
        return self._convert_result("Party Planner", budget, self.ai.generate_json(prompt), True)

    def jewelry(self, data, image_file=None):
        budget = clean_number(data.get("budget"), "Budget", 1)
        occasion = str(data.get("occasion", "")).strip()
        style = str(data.get("style", "")).strip()
        if not occasion:
            raise ValueError("Occasion is required")
        if not style:
            raise ValueError("Style is required")

        image_bytes = image_file.read() if image_file else None
        mime_type = image_file.mimetype if image_file else None

        if not self.ai.is_configured():
            return jewelry_mock(budget, occasion, style, bool(image_bytes))

        prompt = f"""Recommend jewelry for an outfit and occasion.
Budget: {budget}
Occasion: {occasion}
Style: {style}
If an image is attached, analyze only visible outfit colors, patterns and styling.
Do not identify the person or infer sensitive traits.
Return JSON only with allocation, recommendations and notes.
Allocation keys: necklace, earrings, bangles, ring, reserve. Total must equal budget."""
        return self._convert_result(
            "Jewelry Planner", budget,
            self.ai.generate_json(prompt, image_bytes, mime_type), True
        )

    def _convert_result(self, planner, budget, payload, ai_powered):
        allocation = payload.get("allocation") or {}
        recommendations = []
        for item in payload.get("recommendations", []):
            recommendations.append(RecommendationItem(
                name=str(item.get("name", "Recommendation")),
                category=str(item.get("category", "General")),
                estimated_price=float(item.get("estimated_price", 0) or 0),
                platform=str(item.get("platform", "Suggested")),
                url=str(item.get("url", "#")),
                reason=str(item.get("reason", "")),
                quantity=int(item.get("quantity", 1) or 1),
            ))
        return PlannerResult(
            planner, budget,
            {str(k): float(v or 0) for k, v in allocation.items()},
            recommendations,
            [str(x) for x in payload.get("notes", [])],
            ai_powered
        )
