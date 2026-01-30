from flask import Blueprint, request, jsonify
from app.services.event_service import process_event

webhook_bp = Blueprint('webhook', __name__, url_prefix='/webhook')

@webhook_bp.route('/receiver', methods=['POST'])
def receiver():
    print(" GITHUB WEBHOOK RECEIVED!")

    event_type = request.headers.get('X-GitHub-Event', 'unknown')
    payload = request.get_json() or {}

    print(f" Event type: {event_type}")

    try:
        process_event(event_type, payload)
        print(" Event saved to MongoDB")
        return jsonify({"status": "success", "event": event_type}), 200
    except Exception as e:
        print(f" Error processing event: {e}")
        return jsonify({"error": str(e)}), 500
