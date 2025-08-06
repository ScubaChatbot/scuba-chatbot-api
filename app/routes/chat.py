import os
import openai
import logging
from flask import Blueprint, request, jsonify
from app.services.chat import generate_rag_answer
from prometheus_flask_exporter import Counter, Histogram


logger = logging.getLogger(__name__)

# Prometheus metrics
chat_requests_total = Counter('chat_requests_total', 'Total number of chat requests')
chat_failed_requests_total = Counter('chat_failed_requests_total', 'Total number of failed chat requests')
chat_response_latency_seconds = Histogram('chat_response_latency_seconds', 'Chat response latency in seconds')

def handle_chat_request(current_user):
    chat_requests_total.inc()
    import time
    start_time = time.time()
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

    try:
        result = generate_rag_answer(input)
        response_message = result["messages"][-1]

        # Handle both dict and object responses
        if isinstance(response_message, dict):
            response_content = response_message.get("content", "Error processing request")
        else:
            response_content = response_message.content

        logger.info(f"Sending chat response to user '{current_user}': {response_content}")
        chat_response_latency_seconds.observe(time.time() - start_time)
        return jsonify({"response": response_content})
    except Exception as e:
        chat_failed_requests_total.inc()
        logger.error(f"Failed to process chat request: {e}")
        chat_response_latency_seconds.observe(time.time() - start_time)
        return jsonify({"response": "Internal server error"}), 500

def create_chat_bp():
    from app.routes.auth import token_required

    chat_bp = Blueprint('chat', __name__)

    @chat_bp.route("/chat", methods=["POST"])
    @token_required
    def chat(current_user):
        return handle_chat_request(current_user)

    return chat_bp
