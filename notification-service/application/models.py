from . import db
from datetime import datetime


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(500), nullable=False)
    notification_type = db.Column(db.String(50), default='email')
    status = db.Column(db.String(20), default='pending')  # pending, sent, failed
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_sent = db.Column(db.DateTime, nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'message': self.message,
            'type': self.notification_type,
            'status': self.status,
            'created': str(self.date_created),
            'sent': str(self.date_sent) if self.date_sent else None
        }
