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
    events = list(
        db.find()
        .sort("timestamp", -1)
        .limit(limit)
    )

    # Format for UI
    for event in events:
        if event.get('timestamp'):
            event['timestamp_display'] = event['timestamp'][:19].replace('T', ' ')

    return events
