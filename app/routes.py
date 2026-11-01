from flask import Blueprint, render_template, redirect, url_for, flash, request

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app import db
from app.forms import RegistrationForm, LoginForm, DonationForm, CharityForm
from app.models import User, Charity, Donation
from app.blockchain import Blockchain

main = Blueprint("main", __name__)

blockchain = Blockchain()

@main.route("/")
def home():

    charities = Charity.query.all()

    total_donations = Donation.query.count()

    total_charities = Charity.query.count()

    total_users = User.query.count()

    total_transactions = Donation.query.filter_by(
        status="Verified"
    ).count()

    recent_donations = Donation.query.order_by(
        Donation.donation_date.desc()
    ).limit(5).all()

    return render_template(
        "index.html",
        charities=charities,
        total_donations=total_donations,
        total_charities=total_charities,
        total_users=total_users,
        total_transactions=total_transactions,
        recent_donations=recent_donations
    )


@main.route("/register", methods=["GET", "POST"])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            flash("Email already registered!", "danger")
            return redirect(url_for("main.register"))

        # Hash password
        hashed_password = generate_password_hash(
            form.password.data
        ).decode("utf-8")

        # Create user
        user = User(
            name=form.name.data,
            email=form.email.data,
            password_hash=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")

        return redirect(url_for("main.home"))

    return render_template("register.html", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password_hash, form.password.data):

            login_user(user)

            flash("Login successful!", "success")

            return redirect(url_for("main.home"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)


@main.route("/donate/<int:charity_id>", methods=["GET", "POST"])
@login_required
def donate(charity_id):

    charity = Charity.query.get_or_404(charity_id)

    form = DonationForm()

    if form.validate_on_submit():

        block = blockchain.create_block({
            "donor": current_user.name,
            "charity": charity.name,
            "amount": float(form.amount.data)
        })

        donation = Donation(
            amount=form.amount.data,
            user_id=current_user.id,
            charity_id=charity.id,
            transaction_hash=block["hash"],
            status="Verified"
        )

        db.session.add(donation)
        db.session.commit()

        flash("Thank you for your donation!", "success")

        return redirect(url_for("main.charities"))

    return render_template(
        "donate.html",
        form=form,
        charity=charity
    )

@main.route("/logout")
@login_required
def logout():

    logout_user()

    flash("You have been logged out.", "info")

    return redirect(url_for("main.home"))


@main.route("/charities")
def charities():

    charities = Charity.query.all()

    return render_template(
        "charities.html",
        charities=charities
    )

@main.route("/history")
@login_required
def history():

    donations = Donation.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Donation.donation_date.desc()
    ).all()

    return render_template(
        "history.html",
        donations=donations
    )



@main.route("/admin")
@login_required
def admin_dashboard():

    if current_user.role != "admin":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("main.home"))

    charities = Charity.query.all()
    donations = Donation.query.all()
    users = User.query.all()

    return render_template(
        "admin_dashboard.html",
        charities=charities,
        donations=donations,
        users=users
    )


@main.route("/admin/add-charity", methods=["GET", "POST"])
@login_required
def add_charity():

    if current_user.role != "admin":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("main.home"))

    form = CharityForm()

    if form.validate_on_submit():

        charity = Charity(
            name=form.name.data,
            description=form.description.data,
            category=form.category.data
        )

        db.session.add(charity)
        db.session.commit()

        flash("Charity added successfully!", "success")

        return redirect(url_for("main.admin_dashboard"))

    return render_template(
        "add_charity.html",
        form=form
    )

@main.route("/admin/edit-charity/<int:charity_id>", methods=["GET", "POST"])
@login_required
def edit_charity(charity_id):

    if current_user.role != "admin":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("main.home"))

    charity = Charity.query.get_or_404(charity_id)

    form = CharityForm(obj=charity)

    if form.validate_on_submit():

        charity.name = form.name.data
        charity.description = form.description.data
        charity.category = form.category.data

        db.session.commit()

        flash("Charity updated successfully!", "success")

        return redirect(url_for("main.admin_dashboard"))

    return render_template(
        "edit_charity.html",
        form=form,
        charity=charity
    )

@main.route("/admin/delete-charity/<int:charity_id>")
@login_required
def delete_charity(charity_id):

    if current_user.role != "admin":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("main.home"))

    charity = Charity.query.get_or_404(charity_id)

    if charity.donations:
        flash(
            "This charity cannot be deleted because it has donation records.",
            "warning"
        )
        return redirect(url_for("main.admin_dashboard"))

    db.session.delete(charity)
    db.session.commit()

    flash("Charity deleted successfully!", "success")

    return redirect(url_for("main.admin_dashboard"))

@main.route("/admin/users")
@login_required
def manage_users():

    if current_user.role != "admin":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("main.home"))

    users = User.query.order_by(User.id).all()

    return render_template(
        "manage_users.html",
        users=users
    )

@main.route("/admin/donations")
@login_required
def admin_donations():

    if current_user.role != "admin":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("main.home"))

    status = request.args.get("status")

    if status:
        donations = Donation.query.filter_by(
            status=status
        ).order_by(
            Donation.donation_date.desc()
        ).all()
    else:
        donations = Donation.query.order_by(
            Donation.donation_date.desc()
        ).all()

    return render_template(
        "admin_donations.html",
        donations=donations,
        selected_status=status
    )