from flask import flash, redirect, render_template, url_for
from com import db
from com.models import User, Item
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_bp
from .forms import RegistrationForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from .email import send_psw_reset_email


@auth_bp.route('/register', methods=["GET", "POST"])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password1.data
                              )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(
            f'Account was created successfully. '
            f'You are now logged in as {user_to_create.username}', category='success'
        )
        return redirect(url_for('main.home_page'))

    if form.errors != {}:
        for err_msg in form.errors:
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@auth_bp.route('/login_page', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        print('===The form is submitted===')
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user is None:
            flash('There is no user with this username. Please, try again', category='danger')
        elif attempted_user.check_login_psw(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! Now you are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('main.home_page'))
        else:
            flash('Username and password are not matched. Please, try again', category='danger')
    return render_template('login_page.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('main.home_page'))


@auth_bp.route('/reset_password_request', methods=["GET", "POST"])
def reset_psw_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data)
        if user:
            send_psw_reset_email(user)
        flash(f'Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login_page'))
    return render_template(url_for('reset_psw_request.html'), title='Reset Password', form=form)


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
        if user.email != form.email.data:
            flash('Email does not match the one associated with the reset request.', category='danger')
        else:
            user.password = form.new_password1.data
            db.session.commit()
            flash('Your password has been reset. Now you can log in', category='success')
            return redirect(url_for('auth.login_page'))
    return render_template('reset_password.html', form=form)

