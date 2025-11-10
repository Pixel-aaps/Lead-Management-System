from flask import Blueprint, request, jsonify, make_response, current_app
from models import User
from utils.jwt_utils import create_token
from models import db
import traceback

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json() or {}
        email = data.get("email", "").strip()
        password = data.get("password", "")

        if not email or not password:
            return jsonify({"error": "Missing email or password"}), 400

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid credentials"}), 401

        # Generate JWT
        token = create_token(user)
        print("✅ JWT created for:", email)

        # Send both cookie + token in JSON response
        resp = make_response(jsonify({
            "success": True,
            "token": token
        }))
        resp.set_cookie(
            'token', token,
            httponly=True,
            secure=current_app.config.get('COOKIE_SECURE', False),
            samesite=current_app.config.get('COOKIE_SAMESITE', 'Lax'),
            max_age=current_app.config.get('JWT_EXP_DELTA_SECONDS', 3600)
        )
        return resp

    except Exception as e:
        print("LOGIN ERROR:", e)
        traceback.print_exc()
        return jsonify({"error": "Server error", "details": str(e)}), 500



@auth_bp.route("/logout", methods=["POST"])
def logout():
    resp = make_response(jsonify({"success": True}))
    resp.delete_cookie('token')
    return resp