import os
import openai
from flask import Blueprint, request, jsonify
from app.routes.auth import token_required
from app.services.chat import generate_rag_answer

chat_bp = Blueprint('chat', __name__)

@chat_bp.route("/chat", methods=["POST"])
@token_required
def chat(current_user):
    data = request.get_json()
    message = data.get("message", "")

    input = {
        "messages": [
            {
            "role": "user",
            "content": message
            }        
        ]
    }

    response = generate_rag_answer(input)["messages"][-1].content

    return response