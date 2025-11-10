import jwt
import datetime
from flask import request, jsonify, current_app

def create_token(user):
    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=current_app.config['JWT_EXP_DELTA_SECONDS'])
    }
    token = jwt.encode(payload, current_app.config['JWT_SECRET'], algorithm=current_app.config['JWT_ALGORITHM'])
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def jwt_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token and 'Authorization' in request.headers:
            token = request.headers.get('Authorization').split('Bearer ')[-1]

        if not token:
            return jsonify({"error": "Missing token"}), 401

        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=[current_app.config['JWT_ALGORITHM']])
            request.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except Exception as e:
            print("JWT decode error:", e)
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated