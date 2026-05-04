# application/product_api/routes.py
from . import product_api_blueprint
from .. import db
from ..models import Product
from flask import jsonify, request


@product_api_blueprint.route('/api/products', methods=['GET'])
def products():
    items = []
    for row in Product.query.all():
        items.append(row.to_json())

    response = jsonify({'results': items})
    return response


@product_api_blueprint.route('/api/product/create', methods=['POST'])
def post_create():
    name = request.form['name']
    slug = request.form['slug']
    image = request.form['image']
    price = request.form['price']

    item = Product()
    item.name = name
    item.slug = slug
    item.image = image
    item.price = price

    db.session.add(item)
    db.session.commit()

    response = jsonify({'message': 'Product added', 'product': item.to_json()})
    return response


@product_api_blueprint.route('/api/product/<slug>', methods=['GET'])
def product(slug):
    item = Product.query.filter_by(slug=slug).first()
    if item is not None:
        response = jsonify({'result': item.to_json()})
    else:
        response = jsonify({'message': 'Cannot find product'}), 404
    return response

from flask import jsonify
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

@product_api_blueprint.route('/health', methods=['GET'])
def product_health():
    return jsonify({'status': 'healthy', 'service': 'product-service'}), 200

@product_api_blueprint.route('/metrics', methods=['GET'])
def product_metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
