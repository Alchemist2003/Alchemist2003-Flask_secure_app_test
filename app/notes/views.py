from flask import Blueprint, render_template, request, session, redirect
from app.models import SecureNote
from app.extensions import db

notes_views = Blueprint("notes_views", __name__)

@notes_views.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        note = SecureNote(
            title="note",
            user_id=session["user_id"]
        )
        note.set_content(request.form["content"])
        db.session.add(note)
        db.session.commit()

    notes = SecureNote.query.filter_by(user_id=session["user_id"]).all()
    return render_template(
        "dashboard.html",
        notes=[n.get_content() for n in notes]
    )
