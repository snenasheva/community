from flask import flash, redirect, render_template, url_for
from com import db
from com.models import User, Item
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_bp
from .forms import RegistrationForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from sqlalchemy.exc import IntegrityError
from .email import send_psw_reset_email, send_verification_email


@auth_bp.route('/register', methods=["GET", "POST"])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():

        user_to_create = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password1.data
        )
        try:
            db.session.add(user_to_create)
            db.session.commit()
            send_verification_email(user_to_create)
            flash(
                    'A verification email has been sent to your email address. Please verify your account.',
                    category='info'
                )
            return redirect(url_for('auth.login_page'))

        except IntegrityError:
            db.session.rollback()
            flash('This email or username is already associated with an account', category='danger')

    if form.errors != {}:
        for field, err_msgs in form.errors.items():
            for err_msg in err_msgs:
                if field in ['username', 'email']:
                    flash("The username or email is already in use. Please try again with different credentials.",
                          category='danger')
                else:
                    flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@auth_bp.route('/verify_email/<token>', methods=["GET", "POST"])
def verify_email(token):
    user = User.verify_reset_psw_token(token)
    if not user:
        flash('The verification link is invalid or has expired', category='danger')
        return redirect(url_for('auth.login_page'))

    if user.verified:
        flash('Your email was already verified', category='info')
    else:
        user.verified = True
        db.session.commit()
        flash('Your registration was completed successfully', category='success')
    db.session.commit()
    return redirect(url_for('auth.login_page'))


@auth_bp.route('/login_page', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        if '@' in form.username_or_email.data:
            attempted_user = User.query.filter_by(email=form.username_or_email.data).first()
        else:
            attempted_user = User.query.filter_by(username=form.username_or_email.data).first()
        if attempted_user is None:
            flash('There is no account associated with this username or email. Please, try again', category='danger')
        elif not attempted_user.verified:
            flash('Your email is not verified. Please check your email to verify your account.', category='warning')
        elif attempted_user.check_login_psw(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! Now you are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('main.home_page'))
        else:
            flash('Username/Email and password do not matched. Please, try again', category='danger')
    return render_template('login_page.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('main.home_page'))


@auth_bp.route('/delete', methods=["GET", "POST"])
@login_required
def delete_account():
    items_to_delete = Item.query.filter_by(owner_id=current_user.id).all()
    for item in items_to_delete:
        db.session.delete(item)
    user_to_delete = User.query.filter_by(username=current_user.username).first()
    db.session.delete(user_to_delete)
    db.session.commit()
    flash('Your account has been deleted', category='info')
    return redirect(url_for('main.home_page'))


@auth_bp.route('/reset_password_request', methods=["GET", "POST"])
def reset_psw_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_psw_reset_email(user)
        flash(f'Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login_page'))
    return render_template('reset_psw_request.html', title='Reset Password', form=form)


@auth_bp.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    user = User.verify_reset_psw_token(token)
    if not user:
        flash('The reset password link is invalid or has expired.', category='danger')
        return redirect(url_for('auth.login_page'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        print("Form validated successfully")
        if user.email != form.email.data:
            flash('Email does not match the one associated with the reset request.', category='danger')
        else:
            print(f'Before: {user.password_hash}')
            user.password = form.new_password1.data
            print(f'After: {user.password_hash}')
            user.verified = True
            db.session.commit()
            print('Password is updated in database')
            flash('Your password has been reset. Now you can log in', category='success')
            return redirect(url_for('auth.login_page'))
    else:
        print(form.errors)
    return render_template('email/reset_password.html', form=form, token=token)

