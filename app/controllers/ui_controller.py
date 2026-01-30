from flask import Blueprint, render_template
from app.repositories.event_repository import get_recent_events

ui_bp = Blueprint('ui', __name__)

@ui_bp.route('/')
def home():
    return '''
    <div style="text-align:center; padding:50px;">
        <h1 style="color:#0366d6;">🚀 GitHub Webhook Server</h1>
        <p><a href="/events" style="font-size:24px;padding:20px;background:#0366d6;color:white;text-decoration:none;border-radius:12px;display:inline-block;">📊 View Events Dashboard</a></p>
        <p style="color:#666;">Webhook endpoint: <code>POST /webhook/receiver</code></p>
    </div>
    '''

@ui_bp.route('/events')
def events_page():
    events = get_recent_events(limit=10)
    return render_template('events.html', events=events)
