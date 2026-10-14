from flask import Blueprint, jsonify, request
from services.planner_service import PlannerService

planner_bp = Blueprint("planner", __name__)
planner_service = PlannerService()

def json_error(message, status=400):
    return jsonify({"success": False, "error": message}), status

@planner_bp.route("/generate-home", methods=["POST"])
def generate_home():
    try:
        result = planner_service.home(request.get_json(silent=True) or {})
        return jsonify({"success": True, "data": result.to_dict()})
    except ValueError as error:
        return json_error(str(error))
    except Exception as error:
        return json_error(f"Home planner failed: {error}", 500)

@planner_bp.route("/generate-party", methods=["POST"])
def generate_party():
    try:
        result = planner_service.party(request.get_json(silent=True) or {})
        return jsonify({"success": True, "data": result.to_dict()})
    except ValueError as error:
        return json_error(str(error))
    except Exception as error:
        return json_error(f"Party planner failed: {error}", 500)

@planner_bp.route("/generate-jewelry", methods=["POST"])
def generate_jewelry():
    try:
        result = planner_service.jewelry(
            request.form.to_dict(),
            request.files.get("outfit_image")
        )
        return jsonify({"success": True, "data": result.to_dict()})
    except ValueError as error:
        return json_error(str(error))
    except Exception as error:
        return json_error(f"Jewelry planner failed: {error}", 500)
