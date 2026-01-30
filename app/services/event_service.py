from app.repositories.event_repository import save_event
from datetime import datetime
import json

def process_event(event_type, payload):
    """Process GitHub webhook payload into normalized event"""

    print("🔍" + "="*60)
    print(f"📨 EVENT TYPE: {event_type}")
    print(f"🔑 PAYLOAD KEYS: {list(payload.keys())}")
    print(f"📦 FULL PAYLOAD: {json.dumps(payload, indent=2)[:1000]}...")

    event_data = {
        'eventtype': 'unknown',
        'author': 'Unknown',
        'frombranch': 'unknown',
        'tobranch': 'unknown',
        'timestamp': datetime.utcnow().isoformat()
    }

    if event_type == 'push':
        print("PROCESSING PUSH")
        event_data.update({
            'eventtype': 'push',
            'author': payload.get('pusher', {}).get('name', payload.get('sender', {}).get('login', 'Unknown')),
            'tobranch': payload.get('ref', '').split('/')[-1] if payload.get('ref') else 'main',
            'timestamp': payload.get('head_commit', {}).get('timestamp', datetime.utcnow().isoformat())
        })

    elif event_type == 'pull_request':
        print(" PROCESSING PULL_REQUEST")
        pr = payload.get('pull_request', {})
        action = payload.get('action', 'unknown')

        print(f" PR STATE: {pr.get('state')}")
        print(f" PR MERGED: {pr.get('merged')}")
        print(f" PR ACTION: {action}")
        print(f" PR USER: {pr.get('user')}")
        print(f" MERGED_BY: {pr.get('merged_by')}")

        if pr.get('merged') is True:
            print(" DETECTED MERGE!")
            event_data.update({
                'eventtype': 'merge',
                'author': pr.get('merged_by', {}).get('login', payload.get('sender', {}).get('login', 'Unknown')),
                'frombranch': pr.get('head', {}).get('ref', 'unknown'),
                'tobranch': pr.get('base', {}).get('ref', 'unknown'),
                'timestamp': pr.get('merged_at') or pr.get('updated_at') or datetime.utcnow().isoformat()
            })
        else:
            print(" DETECTED REGULAR PR")
            event_data.update({
                'eventtype': 'pull_request',
                'author': pr.get('user', {}).get('login', payload.get('sender', {}).get('login', 'Unknown')),
                'frombranch': pr.get('head', {}).get('ref', 'unknown'),
                'tobranch': pr.get('base', {}).get('ref', 'unknown'),
                'timestamp': pr.get('created_at') or pr.get('updated_at') or datetime.utcnow().isoformat()
            })

    # 🛡️ FINAL VALIDATION
    print(" FINAL EVENT DATA:", event_data)
    save_event(event_data)
    print("" + "="*60)
    return event_data
