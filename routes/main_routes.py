from sqlalchemy import func
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from model import ContactMessage, Prediction, User, db

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("home.html")


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        message = request.form.get("message", "").strip()

        if not all([name, email, message]):
            flash("All contact fields are required.", "warning")
        else:
            db.session.add(ContactMessage(name=name, email=email, message=message))
            db.session.commit()
            flash("Message sent successfully.", "success")
            return redirect(url_for("main.contact"))

    return render_template("contact.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    prediction_count = Prediction.query.filter_by(user_id=current_user.id).count()
    latest_predictions = (
        Prediction.query.filter_by(user_id=current_user.id)
        .order_by(Prediction.created_at.desc())
        .limit(5)
        .all()
    )

    trend_rows = (
        db.session.query(Prediction.predicted_disease, func.count(Prediction.id))
        .filter(Prediction.user_id == current_user.id)
        .group_by(Prediction.predicted_disease)
        .all()
    )

    chart_labels = [row[0] for row in trend_rows]
    chart_values = [row[1] for row in trend_rows]

    return render_template(
        "dashboard.html",
        prediction_count=prediction_count,
        latest_predictions=latest_predictions,
        chart_labels=chart_labels,
        chart_values=chart_values,
    )


@main_bp.route("/history")
@login_required
def history():
    records = (
        Prediction.query.filter_by(user_id=current_user.id)
        .order_by(Prediction.created_at.desc())
        .all()
    )
    return render_template("history.html", records=records)


@main_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        old_password = request.form.get("old_password", "")
        new_password = request.form.get("new_password", "")

        if name:
            current_user.name = name

        if old_password and new_password:
            if current_user.check_password(old_password) and len(new_password) >= 8:
                current_user.set_password(new_password)
            else:
                flash("Password update failed. Check credentials/rules.", "danger")
                return redirect(url_for("main.profile"))

        db.session.commit()
        flash("Profile updated.", "success")
        return redirect(url_for("main.profile"))

    return render_template("profile.html")


@main_bp.route("/admin")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash("Admin access only.", "danger")
        return redirect(url_for("main.dashboard"))

    user_count = User.query.count()
    prediction_count = Prediction.query.count()
    contacts_count = ContactMessage.query.count()
    return render_template(
        "admin_dashboard.html",
        user_count=user_count,
        prediction_count=prediction_count,
        contacts_count=contacts_count,
    )
