from app.extensions import get_db

def save_event(event_data):
    """Save GitHub event (Repository layer)"""
    db = get_db()
    result = db.insert_one(event_data)
    print(f" Saved event ID: {result.inserted_id}")
    return str(result.inserted_id)

def get_recent_events(limit=10):
    """Fetch recent events (Repository layer)"""
    db = get_db()

    #  FIX: Convert Cursor → List
    cursor = db.find().sort("timestamp", -1).limit(limit)
    events = list(cursor)  #  REQUIRED! Cursor ≠ List

    print(f" Found {len(events)} events in DB")  # Debug

    # Format for UI
    for event in events:
        if event.get('timestamp'):
            # Fix timestamp format for display
            event['timestamp_display'] = event['timestamp'].replace('T', ' ').split('.')[0]

    return events


