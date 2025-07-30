
from flask import Blueprint, request, jsonify
from app.routes.auth import token_required

chat_bp = Blueprint('chat', __name__)

@chat_bp.route("/chat", methods=["POST"])
@token_required
def chat(current_user):
    data = request.get_json()
    message = data.get("message", "")

    # Temporary logic
    return jsonify({"response": f"Received your message: {message}"})