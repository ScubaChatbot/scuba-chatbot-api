

import os
import openai
from flask import Blueprint, request, jsonify
from app.routes.auth import token_required

chat_bp = Blueprint('chat', __name__)

@chat_bp.route("/chat", methods=["POST"])
@token_required
def chat(current_user):
    data = request.get_json()
    message = data.get("message", "")

    openai.api_key = os.environ.get("OPENAI_API_KEY")
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a polite, customer-focused scuba diving assistant for Colombia. Always answer in a friendly and helpful way."},
                {"role": "user", "content": message}
            ],
            max_tokens=200
        )
        reply = response.choices[0].message.content
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500