from flask import jsonify, request, make_response
from . import notification_api_blueprint
from .. import db
from ..models import Notification
from datetime import datetime
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST


@notification_api_blueprint.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'notification-service'}), 200


@notification_api_blueprint.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


@notification_api_blueprint.route('/api/notifications', methods=['GET'])
def get_notifications():
    user_id = request.args.get('user_id')
    if user_id:
        items = Notification.query.filter_by(user_id=user_id).all()
    else:
        items = Notification.query.all()
    return jsonify([n.to_json() for n in items])


@notification_api_blueprint.route('/api/notifications/send', methods=['POST'])
def send_notification():
    data = request.get_json()
    if not data or 'user_id' not in data or 'message' not in data:
        return make_response(jsonify({'error': 'user_id and message required'}), 400)

    notification = Notification()
    notification.user_id = data['user_id']
    notification.message = data['message']
    notification.notification_type = data.get('type', 'email')
    notification.status = 'sent'
    notification.date_sent = datetime.utcnow()

    db.session.add(notification)
    db.session.commit()

    return jsonify({'result': notification.to_json(), 'message': 'Notification sent (simulated)'}), 201


@notification_api_blueprint.route('/api/notifications/<int:notification_id>', methods=['GET'])
def get_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    return jsonify(notification.to_json())
