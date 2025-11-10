from flask import Blueprint, request, jsonify
from models import Lead, db
from utils.jwt_utils import jwt_required
from utils.validators import validate_lead

leads_bp = Blueprint('leads', __name__)

@leads_bp.route("", methods=["GET"])
@leads_bp.route("/", methods=["GET"])
@jwt_required
def get_leads():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400

    search = request.args.get('search', '').strip().lower()
    query = Lead.query
    if search:
        query = query.filter(
            db.or_(
                db.func.lower(Lead.name).like(f"%{search}%"),
                db.func.lower(Lead.email).like(f"%{search}%")
            )
        )

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "leads": [
            {"id": l.id, "name": l.name, "email": l.email, "phone": l.phone, "status": l.status}
            for l in paginated.items
        ],
        "page": page,
        "per_page": per_page,
        "total": paginated.total
    })

@leads_bp.route("", methods=["POST"])
@leads_bp.route("/", methods=["POST"])
@jwt_required
def create_lead():
    data = request.get_json() or {}
    errors = validate_lead(data)
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    name = data["name"].strip()
    email = data["email"].strip()

    duplicate = Lead.query.filter(
        db.or_(Lead.name == name, Lead.email == email)
    ).first()
    if duplicate:
        dup_field = "name" if duplicate.name == name else "email"
        return jsonify({"error": f"A lead with the same {dup_field} already exists."}), 400

    lead = Lead(
        name=name,
        email=email,
        phone=data.get("phone", "").strip(),
        status=data.get("status", "New")
    )
    db.session.add(lead)
    db.session.commit()

    return jsonify({
        "lead": {"id": lead.id, "name": lead.name, "email": lead.email, "phone": lead.phone, "status": lead.status}
    }), 201

@leads_bp.route("/<int:lead_id>", methods=["PUT"])
@jwt_required
def update_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    data = request.get_json() or {}

    errors = validate_lead(data, partial=True)
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    for field in ['name', 'email', 'phone', 'status']:
        if field in data:
            setattr(lead, field, data[field])

    db.session.commit()
    return jsonify({
        "lead": {"id": lead.id, "name": lead.name, "email": lead.email, "phone": lead.phone, "status": lead.status}
    })

@leads_bp.route("/<int:lead_id>", methods=["DELETE"])
@jwt_required
def delete_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    db.session.delete(lead)
    db.session.commit()
    return jsonify({"deleted": True})
