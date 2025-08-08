from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint. Returns 200 OK if the service is up.
    """
    return jsonify({"status": "ok"}), 200
