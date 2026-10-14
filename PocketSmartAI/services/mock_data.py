from models import PlannerResult, RecommendationItem

def home_mock(budget, rooms):
    allocation = {
        "furniture": round(budget * 0.40, 2),
        "decor": round(budget * 0.20, 2),
        "lighting": round(budget * 0.15, 2),
        "storage": round(budget * 0.15, 2),
        "reserve": round(budget * 0.10, 2),
    }
    recommendations = [
        RecommendationItem("Modern Sofa", "Furniture", 18000, "Amazon", "https://www.amazon.in/", "Good for living-room comfort."),
        RecommendationItem("LED Ceiling Light", "Lighting", 2500, "Flipkart", "https://www.flipkart.com/", "Energy-efficient lighting."),
        RecommendationItem("Decorative Wall Art", "Decor", 1800, "Amazon", "https://www.amazon.in/", "Adds a simple premium look."),
        RecommendationItem("Storage Cabinet", "Storage", 6500, "IKEA", "https://www.ikea.com/in/en/", "Useful for organized storage."),
    ]
    return PlannerResult("Home Interior Planner", budget, allocation, recommendations,
                         [f"Rooms/items considered: {', '.join(rooms) or 'General home setup'}.",
                          "Prices are sample estimates, not live marketplace prices."], False)

def party_mock(budget, guests, event_type, venue):
    allocation = {
        "venue": round(budget * 0.20, 2),
        "catering": round(budget * 0.40, 2),
        "decor": round(budget * 0.15, 2),
        "entertainment": round(budget * 0.15, 2),
        "venue_stay": round(budget * 0.10, 2),
    }
    recommendations = [
        RecommendationItem("Catering Package", "Catering", round(budget*.40,2), "Swiggy", "https://www.swiggy.com/", f"Planned for about {guests} guests."),
        RecommendationItem("Event Decoration", "Decor", round(budget*.15,2), "Zomato", "https://www.zomato.com/", "Sample vendor allocation."),
        RecommendationItem("DJ / Music Setup", "Entertainment", round(budget*.15,2), "Local Vendor", "#", "Sample entertainment allocation."),
    ]
    return PlannerResult("Party Planner", budget, allocation, recommendations,
                         [f"Event: {event_type}. Venue: {venue}.", "Allocations are sample planning estimates."], False)

def jewelry_mock(budget, occasion, style, image_attached):
    allocation = {"necklace": round(budget*.35,2), "earrings": round(budget*.25,2),
                  "bangles": round(budget*.20,2), "ring": round(budget*.10,2),
                  "reserve": round(budget*.10,2)}
    recommendations = [
        RecommendationItem("Elegant Necklace Set", "Necklace", allocation["necklace"], "Amazon", "https://www.amazon.in/", f"Suitable for {occasion}."),
        RecommendationItem("Matching Earrings", "Earrings", allocation["earrings"], "Flipkart", "https://www.flipkart.com/", f"Matches {style} styling."),
        RecommendationItem("Classic Bangles", "Bangles", allocation["bangles"], "Amazon", "https://www.amazon.in/", "Flexible styling option."),
    ]
    notes = [
        f"Occasion: {occasion}. Preferred style: {style}.",
        "Image was considered as an optional outfit reference." if image_attached else "No outfit image was supplied.",
        "Prices are sample estimates, not live jewelry prices."
    ]
    return PlannerResult("Jewelry Planner", budget, allocation, recommendations, notes, False)
