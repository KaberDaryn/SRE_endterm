from flask import jsonify, request, make_response
from . import payment_api_blueprint
from .. import db
from ..models import Payment
from datetime import datetime
import uuid
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST


@payment_api_blueprint.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'payment-service'}), 200


@payment_api_blueprint.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


@payment_api_blueprint.route('/api/payments', methods=['GET'])
def get_payments():
    user_id = request.args.get('user_id')
    if user_id:
        payments = Payment.query.filter_by(user_id=user_id).all()
    else:
        payments = Payment.query.all()
    return jsonify([p.to_json() for p in payments])


@payment_api_blueprint.route('/api/payments/process', methods=['POST'])
def process_payment():
    data = request.get_json()
    required = ['order_id', 'user_id', 'amount']
    if not data or not all(k in data for k in required):
        return make_response(jsonify({'error': 'order_id, user_id and amount required'}), 400)

    payment = Payment()
    payment.order_id = data['order_id']
    payment.user_id = data['user_id']
    payment.amount = data['amount']
    payment.currency = data.get('currency', 'USD')
    payment.payment_method = data.get('payment_method', 'card')
    payment.transaction_id = str(uuid.uuid4())
    payment.status = 'completed'  # simulated success

    db.session.add(payment)
    db.session.commit()

    return jsonify({
        'result': payment.to_json(),
        'message': 'Payment processed successfully (simulated)'
    }), 201


@payment_api_blueprint.route('/api/payments/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    return jsonify(payment.to_json())


@payment_api_blueprint.route('/api/payments/<int:payment_id>/refund', methods=['POST'])
def refund_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    if payment.status != 'completed':
        return make_response(jsonify({'error': 'Only completed payments can be refunded'}), 400)
    payment.status = 'refunded'
    db.session.commit()
    return jsonify({'result': payment.to_json(), 'message': 'Refund processed (simulated)'})
