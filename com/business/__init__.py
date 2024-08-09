from flask import Blueprint, redirect, url_for, render_template

business_bp = Blueprint('business', __name__)

from . import routes
