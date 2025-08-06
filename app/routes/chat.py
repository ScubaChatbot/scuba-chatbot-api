import os
import openai
import logging
from flask import Blueprint, request, jsonify
from app.services.chat import generate_rag_answer

logger = logging.getLogger(__name__)

def handle_chat_request(current_user):
    data = request.get_json()
    message = data.get("message", "")
    logger.info(f"Received chat request from user '{current_user}': {message}")

    input = {
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ]
    }

    result = generate_rag_answer(input)
    response_message = result["messages"][-1]

    # Handle both dict and object responses
    if isinstance(response_message, dict):
        response_content = response_message.get("content", "Error processing request")
    else:
        response_content = response_message.content

    logger.info(f"Sending chat response to user '{current_user}': {response_content}")
    return jsonify({"response": response_content})

def create_chat_bp():
    from app.routes.auth import token_required

    chat_bp = Blueprint('chat', __name__)

    @chat_bp.route("/chat", methods=["POST"])
    @token_required
    def chat(current_user):
        return handle_chat_request(current_user)

    return chat_bp
