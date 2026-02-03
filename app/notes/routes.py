from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# ✅ RELATIVE imports
from ..extensions import db
from ..models import SecureNote

notes_bp = Blueprint("notes", __name__, url_prefix="/notes")


@notes_bp.route("/", methods=["POST"])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.json

    note = SecureNote(title=data["title"], user_id=user_id)
    note.set_content(data["content"])  # 🔐 encrypted

    db.session.add(note)
    db.session.commit()

    return jsonify({"msg": "Note created"}), 201


@notes_bp.route("/", methods=["GET"])
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()
    notes = SecureNote.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "id": note.id,
            "title": note.title,
            "content": note.get_content(),  # 🔓 decrypted
            "created_at": note.created_at.isoformat()
        }
        for note in notes
    ])
