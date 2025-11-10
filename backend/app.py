# backend/app.py
import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from models import db, User
from routes.auth import auth_bp
from routes.leads import leads_bp
from config import Config

app = Flask(__name__, static_folder=None)
app.config.from_object(Config)

from flask_cors import CORS

frontend_origin = app.config.get("FRONTEND_URL")
if frontend_origin:
    CORS(
        app,
        supports_credentials=True,
        origins=[frontend_origin],
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )
    print(f"CORS enabled for {frontend_origin} with credentials")
else:
    CORS(app)
    print("⚠️ CORS: FRONTEND_URL not set. Using permissive mode without credentials.")


db.init_app(app)

with app.app_context():
    db.create_all()
    # Create default user if not exists
    if not User.query.filter_by(email="user@gmail.com").first():
        u = User(email="user@gmail.com", name="User")
        u.set_password("1234")
        db.session.add(u)
        db.session.commit()
        print("Default user created: user@gmail.com / 1234")

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(leads_bp, url_prefix="/api/leads")

# serve static frontend files (if you put frontend next to backend)
@app.route('/')
def serve_index():
    frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_dir, 'login.html')

@app.route('/login')
def serve_login():
    frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_dir, 'login.html')

@app.route('/leads')
def serve_leads():
    frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_dir, 'leads.html')

@app.route('/<path:filename>')
def serve_static(filename):
    frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_dir, filename)

if __name__ == "__main__":
    # Port env var provided by Render
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
