from flask import render_template, redirect, url_for, flash
from com import db
from com.models import Item
from flask_login import login_required, current_user
from . import business_bp
from .forms import BusinessForm


@business_bp.route('/business', methods=["GET", "POST"])
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
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'There was an error with creating a user for field "{getattr(form, field).label.text}": {error}',
                      category='danger')
                print("Form Errors:", form.errors)
    return render_template('business.html', form=form)


@business_bp.route('/service/<url>')
def service(url):
    item = Item.query.filter_by(url_friendly_name=url).first_or_404()
    return render_template('service.html', item=item)


@business_bp.route('/service/edit/<url>', methods=["GET", "POST"])
@login_required
def edit_service(url):
    item = Item.query.filter_by(url_friendly_name=url, owner_id=current_user.id).first_or_404()
    form = BusinessForm(obj=item)
    form.submit.label.text = "Save changes"
    if form.validate_on_submit():
        item.name = form.business_name.data
        item.url_friendly_name = form.business_name.data.replace(' ', '').lower()
        item.category = form.category.data
        item.description = form.description.data
        item.phone = form.phone.data
        item.address = form.address.data
        item.web_page = form.web_page.data
        item.owner_name = form.owner_name.data
        db.session.commit()
        flash(f'The page was edited successfully', category='success')
        return redirect(url_for('business.service', url=item.url_friendly_name))
    return render_template('edit.html', form=form, item=item)


@business_bp.route('/service/delete/<url>', methods=["POST"])
@login_required
def delete_service(url):
    item = Item.query.filter_by(url_friendly_name=url, owner_id=current_user.id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    flash('Your business page has been deleted', category='info')
    return redirect(url_for('main.home_page'))



