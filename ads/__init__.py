from flask import Blueprint

ads_bp = Blueprint('ads', __name__, url_prefix='/ads')
print("Blueprint 'ads' створено")

from .routes import add, edit, delete, filter, pagination, search, sorting, comments, ratings, ad_detail