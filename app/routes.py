import secrets

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
)
from flask_login import login_user, logout_user, login_required, current_user

from .extensions import db
from .models import User, LawyerProfile, Issue, Chat, Message, ISSUE_CATEGORIES

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        if current_user.is_lawyer:
            return redirect(url_for("main.lawyer_dashboard"))
        return redirect(url_for("main.user_dashboard"))
    return render_template("landing.html")


@main_bp.route("/signup/user", methods=["GET", "POST"])
def signup_user():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return redirect(url_for("main.signup_user"))

        user = User(name=name, email=email, is_lawyer=False)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Account created. Please log in.", "success")
        return redirect(url_for("main.login"))

    return render_template("signup_user.html")


@main_bp.route("/signup/lawyer", methods=["GET", "POST"])
def signup_lawyer():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        expertise = request.form.getlist("expertise")
        experience_description = request.form.get("experience_description")

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return redirect(url_for("main.signup_lawyer"))

        user = User(name=name, email=email, is_lawyer=True)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        profile = LawyerProfile(
            user_id=user.id,
            expertise_categories=",".join(expertise),
            experience_description=experience_description,
        )
        db.session.add(profile)
        db.session.commit()

        flash("Lawyer account created. Please log in.", "success")
        return redirect(url_for("main.login"))

    return render_template("signup_lawyer.html", categories=ISSUE_CATEGORIES)


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully.", "success")
            if user.is_lawyer:
                return redirect(url_for("main.lawyer_dashboard"))
            return redirect(url_for("main.user_dashboard"))

        flash("Invalid email or password.", "error")

    return render_template("login.html")


@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.index"))


@main_bp.route("/dashboard/user")
@login_required
def user_dashboard():
    if current_user.is_lawyer:
        return redirect(url_for("main.lawyer_dashboard"))

    issues = Issue.query.filter_by(user_id=current_user.id).order_by(
        Issue.created_at.desc()
    )
    chats = Chat.query.filter_by(user_id=current_user.id).order_by(
        Chat.created_at.desc()
    )
    return render_template("user_dashboard.html", issues=issues, chats=chats)


@main_bp.route("/dashboard/lawyer")
@login_required
def lawyer_dashboard():
    if not current_user.is_lawyer:
        return redirect(url_for("main.user_dashboard"))

    profile = current_user.lawyer_profile
    chats = Chat.query.filter_by(lawyer_id=current_user.id).order_by(
        Chat.created_at.desc()
    )
    return render_template("lawyer_dashboard.html", profile=profile, chats=chats)


@main_bp.route("/issue/new", methods=["GET", "POST"])
@login_required
def submit_issue():
    if current_user.is_lawyer:
        flash("Only regular users can submit issues.", "error")
        return redirect(url_for("main.lawyer_dashboard"))

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        category = request.form.get("category")

        if category not in ISSUE_CATEGORIES:
            flash("Invalid category.", "error")
            return redirect(url_for("main.submit_issue"))

        issue = Issue(
            user_id=current_user.id,
            title=title,
            description=description,
            category=category,
        )
        db.session.add(issue)
        db.session.commit()

        flash("Issue submitted.", "success")
        return redirect(url_for("main.lawyer_matches", issue_id=issue.id))

    return render_template("submit_issue.html", categories=ISSUE_CATEGORIES)


@main_bp.route("/issue/<int:issue_id>/lawyers")
@login_required
def lawyer_matches(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    if issue.user_id != current_user.id:
        flash("You do not have access to this issue.", "error")
        return redirect(url_for("main.user_dashboard"))

    # Match lawyers whose expertise includes the issue category
    matching_lawyers = (
        LawyerProfile.query.filter(
            LawyerProfile.expertise_categories.like(f"%{issue.category}%")
        )
        .join(User)
        .all()
    )
    return render_template(
        "lawyer_matches.html", issue=issue, lawyers=matching_lawyers
    )


@main_bp.route("/start_chat/<int:issue_id>/<int:lawyer_id>", methods=["POST"])
@login_required
def start_chat(issue_id, lawyer_id):
    issue = Issue.query.get_or_404(issue_id)
    if issue.user_id != current_user.id:
        flash("You do not have access to this issue.", "error")
        return redirect(url_for("main.user_dashboard"))

    lawyer = User.query.get_or_404(lawyer_id)
    if not lawyer.is_lawyer:
        flash("Selected user is not a lawyer.", "error")
        return redirect(url_for("main.lawyer_matches", issue_id=issue.id))

    chat = Chat.query.filter_by(
        user_id=current_user.id, lawyer_id=lawyer.id, issue_id=issue.id
    ).first()
    if not chat:
        chat = Chat(user_id=current_user.id, lawyer_id=lawyer.id, issue_id=issue.id)
        db.session.add(chat)
        db.session.commit()

    return redirect(url_for("main.chat_view", chat_id=chat.id))


def _user_can_access_chat(chat: Chat, user: User) -> bool:
    return user.id in {chat.user_id, chat.lawyer_id}


@main_bp.route("/chat/<int:chat_id>", methods=["GET", "POST"])
@login_required
def chat_view(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if not _user_can_access_chat(chat, current_user):
        flash("You do not have access to this chat.", "error")
        return redirect(url_for("main.index"))

    if request.method == "POST":
        content = request.form.get("content", "").strip()
        if content:
            role = "lawyer" if current_user.is_lawyer else "user"
            msg = Message(
                chat_id=chat.id,
                sender_id=current_user.id,
                sender_role=role,
                content=content,
            )
            db.session.add(msg)
            db.session.commit()
            return redirect(url_for("main.chat_view", chat_id=chat.id))

    messages = chat.messages.all()
    return render_template(
        "chat.html",
        chat=chat,
        messages=messages,
    )


@main_bp.route("/chat/<int:chat_id>/generate_link", methods=["POST"])
@login_required
def generate_jitsi_link(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if not _user_can_access_chat(chat, current_user):
        flash("You do not have access to this chat.", "error")
        return redirect(url_for("main.index"))

    if not chat.jitsi_link:
        random_string = secrets.token_urlsafe(10)
        chat.jitsi_link = f"https://meet.jit.si/{random_string}"
        db.session.commit()

    flash("Video call link generated.", "success")
    return redirect(url_for("main.chat_view", chat_id=chat.id))



