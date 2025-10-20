from app import app, db
from models import ShippingService, ShippingRate

with app.app_context():
    db.drop_all()
    db.create_all()
    
    hoy = ShippingService(name='Envío Hoy', code='ENVIO_HOY', active=True, start_hour=0, end_hour=18)
    prog = ShippingService(name='Envío Programado', code='ENVIO_PROGRAMADO', active=True)
    db.session.add_all([hoy, prog])
    db.session.flush()
    
    for srv in [hoy, prog]:
        db.session.add_all([
            ShippingRate(service_id=srv.id, min_km=0, max_km=3, price=3500, active=True),
            ShippingRate(service_id=srv.id, min_km=3, max_km=4, price=4500, active=True),
            ShippingRate(service_id=srv.id, min_km=4, max_km=5, price=5000, active=True),
            ShippingRate(service_id=srv.id, min_km=5, max_km=6, price=5500, active=True),
            ShippingRate(service_id=srv.id, min_km=6, max_km=7, price=6500, active=True),
        ])
    
    db.session.commit()
    print("✅ Database initialized")
