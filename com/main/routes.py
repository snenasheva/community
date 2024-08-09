from flask import render_template, redirect, url_for, request
from com.models import Item
from . import main_bp


@main_bp.route('/')
@main_bp.route('/home')
def home_page():
    return render_template('home.html')


@main_bp.route('/drop')
def drop():
    return render_template('drop.html')


@main_bp.route('/search', methods=["GET", "POST"])
def search():
    search_query = request.args.get('search_query')
    if search_query:
        results = Item.query.filter(Item.name.ilike(f'%{search_query}%')).all()
        return render_template('search_results.html', results=results, search_query=search_query)
    return redirect(url_for('home_page'))


@main_bp.route('/categories')
def categories_page():
    return render_template('categories.html')


@main_bp.route('/categories/<category_name>')
def items_by_category(category_name):
    items = Item.query.filter_by(category=category_name).all()
    return render_template('category_choice.html', items=items, category_name=category_name)
