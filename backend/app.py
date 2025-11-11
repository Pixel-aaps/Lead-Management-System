import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from models import db, User
from routes.auth import auth_bp
from routes.leads import leads_bp
from config import Config

app = Flask(__name__, static_folder=None)
app.config.from_object(Config)

# --- CORS Configuration ---
frontend_origin = app.config.get("FRONTEND_URL")

if frontend_origin:
    CORS(
        app,
        resources={r"/api/*": {"origins": [frontend_origin]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )
    print(f"✅ CORS enabled for origin: {frontend_origin}")
else:
    CORS(app)
    print("⚠️ CORS: FRONTEND_URL not set. Using permissive mode without credentials.")

# --- Database Initialization ---
db.init_app(app)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(email="user@gmail.com").first():
        u = User(email="user@gmail.com", name="User")
        u.set_password("1234")
        db.session.add(u)
        db.session.commit()
        print("Default user created: user@gmail.com / 1234")

# --- Register Blueprints without trailing slash redirects ---
app.url_map.strict_slashes = False  # Important to prevent 308 redirects

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(leads_bp, url_prefix="/api/leads")

# --- Serve Frontend Files ---
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')

@app.route('/')
@app.route('/login')
def serve_login():
    return send_from_directory(FRONTEND_DIR, 'login.html')

@app.route('/leads')
def serve_leads():
    return send_from_directory(FRONTEND_DIR, 'leads.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(FRONTEND_DIR, filename)

# --- Run the App ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
