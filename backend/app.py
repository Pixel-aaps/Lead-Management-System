from flask import Flask, send_from_directory
from flask_cors import CORS
from models import db, User
from routes.auth import auth_bp
from routes.leads import leads_bp
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True  
CORS(app,supports_credentials=True)

# ✅ Initialize database
db.init_app(app)

with app.app_context():
    db.create_all()
    # Create default user if not exists
    if not User.query.filter_by(email="user@gmail.com").first():
        u = User(email="user@gmail.com", name="User")
        u.set_password("1234")
        db.session.add(u)
        db.session.commit()
        print("✅ Default user created: user@gmail.com / 1234")

# ✅ Register routes
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(leads_bp, url_prefix="/api/leads")

@app.route('/')
def serve_index():
    frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_dir, 'login.html')

@app.route('/<path:filename>')
def serve_static(filename):
    frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_dir, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
