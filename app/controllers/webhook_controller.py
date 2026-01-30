from flask import Blueprint, request
from app.services.event_service import process_event

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook/receiver', methods=['POST'])
def receive_webhook():
    print(" GITHUB RAW REQUEST:")
    print(f"Headers: {dict(request.headers)}")
    print(f"Content-Type: {request.content_type}")
    print(f"Body preview: {request.get_data()[:500]}")

    try:
        #  FIX: Handle Flask 3.0+ JSON parsing
        if request.is_json:
            payload = request.get_json()
        else:
            payload = request.get_json(force=True)  # Force parse non-JSON

        event_type = request.headers.get('X-GitHub-Event', 'unknown')
        print(f"Event type: {event_type}")

        process_event(event_type, payload)
        print(" Event saved to MongoDB")
        return "OK", 200

    except Exception as e:
        print(f" WEBHOOK ERROR: {e}")
        return f"Error: {e}", 500
