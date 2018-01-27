from flask import Blueprint, render_template, jsonify, redirect, url_for

hotel_blueprint = Blueprint('HotelBlueprint', __name__, url_prefix='/hotels')

from .quick_search import QuickSearch

SUPPORTED_PROVIDERS = [
    'Expedia',
    'Orbitz',
    'Priceline',
    'Travelocity',
    'Hilton'
]

@hotel_blueprint.route('/search')
def search():
    results = QuickSearch(
        SUPPORTED_PROVIDERS
    ).get_all()

    return jsonify(
        {'results': results}
    )


@hotel_blueprint.route('/', defaults={'page': 'index'})
def index(page):
    return redirect(url_for('HotelBlueprint.search'))
