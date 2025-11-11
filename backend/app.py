# app.py  (or backend/main.py)
import os
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from models import db, User
from routes.auth import auth_bp
from routes.leads import leads_bp
from config import Config

app = Flask(__name__, static_folder=None)
app.config.from_object(Config)

# ----------------------------------------------------------------------
# 1. CORS – allow the exact Vercel (and localhost) origins
# ----------------------------------------------------------------------
ALLOWED_ORIGINS = [
    # Production Vercel URL (replace with your real one if it changes)
    "https://leadfront-8fsrci3gh-avaneesh6404-3847s-projects.vercel.app",
    # Development / Vercel preview URLs
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# If you still want a fallback from env, keep it – otherwise we hard-code
FRONTEND_URL = app.config.get("FRONTEND_URL")
if FRONTEND_URL:
    ALLOWED_ORIGINS.append(FRONTEND_URL)

CORS(
    app,
    resources={r"/api/*": {"origins": ALLOWED_ORIGINS}},
    supports_credentials=True,                 # needed for cookies / Authorization header
    expose_headers=["Content-Type", "Authorization"],
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
)
print(f"CORS enabled for: {', '.join(ALLOWED_ORIGINS)}")

# ----------------------------------------------------------------------
# 2. Database init + default user
# ----------------------------------------------------------------------
db.init_app(app)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(email="user@gmail.com").first():
        u = User(email="user@gmail.com", name="User")
        u.set_password("1234")          # <-- make sure set_password hashes the pwd!
        db.session.add(u)
        db.session.commit()
        print("Default user created: user@gmail.com / 1234")

# ----------------------------------------------------------------------
# 3. Blueprint registration (no trailing-slash redirects)
# ----------------------------------------------------------------------
app.url_map.strict_slashes = False

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(leads_bp, url_prefix="/api/leads")

# ----------------------------------------------------------------------
# 4. Serve the built React/Vite/whatever frontend
# ----------------------------------------------------------------------
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

@app.route("/")
@app.route("/login")
def serve_login():
    return send_from_directory(FRONTEND_DIR, "login.html")

@app.route("/leads")
def serve_leads():
    return send_from_directory(FRONTEND_DIR, "leads.html")

@app.route("/<path:filename>")
def serve_static(filename):
    """Serve any other static file (JS, CSS, images, etc.)"""
    return send_from_directory(FRONTEND_DIR, filename)

# ----------------------------------------------------------------------
# 5. OPTIONAL: Health-check endpoint (helps Render wake-up)
# ----------------------------------------------------------------------
@app.route("/health")
def health():
    return jsonify({"status": "ok", "timestamp": os.getenv("RENDER_INSTANCE_ID")})

# ----------------------------------------------------------------------
# 6. Global error handlers – return JSON instead of HTML
# ----------------------------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

# ----------------------------------------------------------------------
# 7. Run (Render sets PORT env var)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Render injects PORT; fallback to 5000 for local dev
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)