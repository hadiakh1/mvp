from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db, login_manager


ISSUE_CATEGORIES = [
    "Harassment",
    "Domestic Violence",
    "Property Issues",
    "Workplace Discrimination",
    "Fraud",
    "Family Disputes",
]


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_lawyer = db.Column(db.Boolean, default=False, nullable=False)

    lawyer_profile = db.relationship(
        "LawyerProfile", back_populates="user", uselist=False
    )
    issues = db.relationship("Issue", back_populates="user", lazy="dynamic")

    sent_chats = db.relationship(
        "Chat", foreign_keys="Chat.user_id", back_populates="user", lazy="dynamic"
    )
    received_chats = db.relationship(
        "Chat", foreign_keys="Chat.lawyer_id", back_populates="lawyer", lazy="dynamic"
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LawyerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    expertise_categories = db.Column(db.String(255), nullable=False)
    experience_description = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, default=0.0, nullable=False)
    profile_picture = db.Column(db.String(255), default="default-avatar.png", nullable=False)

    user = db.relationship("User", back_populates="lawyer_profile")

    def categories_list(self):
        return [c.strip() for c in self.expertise_categories.split(",") if c.strip()]


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="issues")
    chat = db.relationship("Chat", back_populates="issue", uselist=False)


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    lawyer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    issue_id = db.Column(db.Integer, db.ForeignKey("issue.id"))
    jitsi_link = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", foreign_keys=[user_id], back_populates="sent_chats")
    lawyer = db.relationship(
        "User", foreign_keys=[lawyer_id], back_populates="received_chats"
    )
    issue = db.relationship("Issue", back_populates="chat")
    messages = db.relationship(
        "Message", back_populates="chat", order_by="Message.created_at", lazy="dynamic"
    )


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    sender_role = db.Column(db.String(20), nullable=False)  # "user" or "lawyer"
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    chat = db.relationship("Chat", back_populates="messages")
    sender = db.relationship("User")



