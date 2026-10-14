from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class RecommendationItem:
    name: str
    category: str
    estimated_price: float
    platform: str
    url: str = "#"
    reason: str = ""
    quantity: int = 1

@dataclass
class PlannerResult:
    planner: str
    budget: float
    allocation: Dict[str, float]
    recommendations: List[RecommendationItem] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    ai_powered: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "planner": self.planner,
            "budget": self.budget,
            "allocation": self.allocation,
            "recommendations": [vars(item) for item in self.recommendations],
            "notes": self.notes,
            "ai_powered": self.ai_powered,
        }

def clean_number(value, field_name: str, minimum: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a valid number")
    if number < minimum:
        raise ValueError(f"{field_name} must be at least {minimum}")
    return number
