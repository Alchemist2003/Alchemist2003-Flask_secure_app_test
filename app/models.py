from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# ✅ RELATIVE imports
from .extensions import db
from .utils.encryption import encrypt_data, decrypt_data


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    notes = db.relationship("SecureNote", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class SecureNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)

    # 🔐 Always encrypted in DB
    encrypted_content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_content(self, plain_text):
        self.encrypted_content = encrypt_data(plain_text)

    def get_content(self):
        return decrypt_data(self.encrypted_content)
