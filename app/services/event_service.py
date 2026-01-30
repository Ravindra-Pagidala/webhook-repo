from app.repositories.event_repository import save_event

def process_event(event_type, payload):
    """Process GitHub webhook payload into normalized event"""
    event_data = {
        'eventtype': None,
        'author': None,
        'frombranch': None,
        'tobranch': None,
        'timestamp': None
    }

    if event_type == 'push':
        event_data.update({
            'eventtype': 'push',
            'author': payload.get('pusher', {}).get('name'),
            'tobranch': payload['ref'].split('/')[-1] if payload.get('ref') else None,
            'timestamp': payload.get('head_commit', {}).get('timestamp')
        })

    elif event_type == 'pull_request':
        pr = payload.get('pull_request', {})
        if pr.get('merged'):
            # Merge event (brownie points!)
            event_data.update({
                'eventtype': 'merge',
                'author': pr.get('merged_by', {}).get('login'),
                'frombranch': pr.get('head', {}).get('ref'),
                'tobranch': pr.get('base', {}).get('ref'),
                'timestamp': pr.get('merged_at')
            })
        else:
            event_data.update({
                'eventtype': 'pull_request',
                'author': pr.get('user', {}).get('login'),
                'frombranch': pr.get('head', {}).get('ref'),
                'tobranch': pr.get('base', {}).get('ref'),
                'timestamp': pr.get('created_at')
            })

    save_event(event_data)
    return event_data
