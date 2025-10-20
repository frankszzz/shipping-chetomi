from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

db = SQLAlchemy()

class ShippingService(db.Model):
    __tablename__ = 'shipping_services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=True)
    start_hour = db.Column(db.Integer)
    end_hour = db.Column(db.Integer)
    rates = db.relationship('ShippingRate', backref='service', lazy=True, cascade='all, delete-orphan')
    
    def is_available_now(self, timezone='America/Santiago'):
        if not self.active:
            return False
        if self.start_hour is None or self.end_hour is None:
            return True
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        return self.start_hour <= now.hour < self.end_hour

class ShippingRate(db.Model):
    __tablename__ = 'shipping_rates'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('shipping_services.id'), nullable=False)
    min_km = db.Column(db.Float, nullable=False)
    max_km = db.Column(db.Float, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)

class DeliveryLog(db.Model):
    __tablename__ = 'delivery_logs'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    from_address = db.Column(db.String(500))
    to_address = db.Column(db.String(500))
    distance_km = db.Column(db.Float)
    service_code = db.Column(db.String(50))
    calculated_price = db.Column(db.Integer)
    order_reference = db.Column(db.String(100))
