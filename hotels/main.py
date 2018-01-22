from flask import Blueprint, render_template, abort

hotel_blueprint =  Blueprint('HotelBlueprint', __name__, url_prefix='/hotels')


@hotel_blueprint.route('/', defaults={'page': 'index'})
def index(page):
    return 'List of things'


@hotel_blueprint.route('/<search_param>')
def search():
    return ''
