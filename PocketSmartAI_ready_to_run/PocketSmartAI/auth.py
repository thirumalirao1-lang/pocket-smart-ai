import secrets
from flask import session

def init_session(app):
    @app.before_request
    def create_session():
        if "session_id" not in session:
            session["session_id"] = secrets.token_urlsafe(24)
