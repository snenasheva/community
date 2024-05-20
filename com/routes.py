from com import app, db
from flask import render_template, url_for, flash, redirect
from com.forms import RegistrationForm, LoginForm, BusinessForm
from com.models import User, Item
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/register', methods=["GET", "POST"])
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
        return redirect(url_for('home_page'))

    if form.errors != {}:
        for err_msg in form.errors:
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login_page', methods=["GET", "POST"])
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
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not matched. Please, try again', category='danger')

    return render_template('login_page.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('home_page'))


@app.route('/business', methods=["GET", "POST"])
@login_required
def business_page():
    form = BusinessForm()
    if form.validate_on_submit():
        business_to_create = Item(name=form.business_name.data,
                                  url_friendly_name=form.business_name.data.replace(' ', '').lower(),
                                  category=form.category.data,
                                  description=form.description.data,
                                  phone=form.phone.data,
                                  address=form.address.data,
                                  web_page=form.web_page.data,
                                  owner_id=current_user.id,
                                  owner_name=form.owner_name.data
                                  )
        db.session.add(business_to_create)
        db.session.commit()
        current_user.has_business_page = True
        db.session.commit()
        flash('Your business page was created successfully', category='success')
        # return redirect(url_for('user_service', url_friendly_name=business_to_create.url_friendly_name))

    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'There was an error with creating a user for field "{getattr(form, field).label.text}": {error}',
                      category='danger')
    print("Form Errors:", form.errors)
    return render_template('business.html', form=form)


@app.route('/service/<url>')
@login_required
def service(url):
    item = Item.query.filter_by(url_friendly_name=url, owner_id=current_user.id).first_or_404()
    return render_template('service.html', item=item)


@app.route('/drop')
def drop():
    return render_template('drop.html')


@app.route('/dropdown')
def dropdown():
    return render_template('dropdown.html')

