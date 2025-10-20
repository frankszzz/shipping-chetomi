from flask import Flask, request, jsonify, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms import IntegerField
from models import db, ShippingService, ShippingRate, DeliveryLog
from services.openroute import OpenRouteService
from config import Config

class ShippingServiceAdmin(ModelView):
    column_list = ('name', 'code', 'active', 'start_hour', 'end_hour')
    column_labels = {
        'name': 'Nombre del Servicio',
        'code': 'Código',
        'active': 'Activo',
        'start_hour': 'Hora Inicio (0-23)',
        'end_hour': 'Hora Fin (0-23)',
        'description': 'Descripción'
    }
    form_columns = ('name', 'code', 'description', 'active', 'start_hour', 'end_hour')
    column_filters = ('active',)
    can_export = True

    # Específico para WTForms
    form_overrides = {
        'start_hour': IntegerField,
        'end_hour': IntegerField
    }

    form_args = {
        'start_hour': {
            'label': 'Hora Inicio (0-23)',
            'validators': [],  # Puedes agregar validadores si quieres
        },
        'end_hour': {
            'label': 'Hora Fin (0-23)',
            'validators': [],
        }
    }

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

admin = Admin(app, name='Shipping Admin', template_mode='bootstrap4', url='/admin')
admin.add_view(ShippingServiceAdmin(ShippingService, db.session, name='Servicios'))
admin.add_view(ModelView(ShippingRate, db.session, name='Tarifas'))
admin.add_view(ModelView(DeliveryLog, db.session, name='Historial'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/shipping/services')
def get_services():
    services = ShippingService.query.filter_by(active=True).all()
    return jsonify({
        "services": [{"service_name": s.name, "service_code": s.code} 
                     for s in services if s.is_available_now()]
    })

@app.route('/shipping/rates', methods=['POST'])
def calculate_rates():
    data = request.json
    req = data.get('request', {})
    from_loc = req.get('from', {})
    to_loc = req.get('to', {})
    
    if not (from_loc.get('latitude') and to_loc.get('latitude')):
        return jsonify({"reference_id": req.get('request_reference'), "rates": []})
    
    ors = OpenRouteService()
    result = ors.calculate_distance(
        {'lat': from_loc['latitude'], 'lon': from_loc['longitude']},
        {'lat': to_loc['latitude'], 'lon': to_loc['longitude']}
    )
    
    if not result or result['distance_km'] > 7:
        return jsonify({"reference_id": req.get('request_reference'), "rates": []})
    
    distance = result['distance_km']
    rates = []
    
    for service in ShippingService.query.filter_by(active=True).all():
        if not service.is_available_now():
            continue
        rate = ShippingRate.query.filter(
            ShippingRate.service_id == service.id,
            ShippingRate.min_km <= distance,
            ShippingRate.max_km > distance
        ).first()
        if rate:
            rates.append({
                "rate_id": f"{service.code}-{rate.id}",
                "rate_description": f"{service.name} - {distance:.1f} km",
                "service_name": service.name,
                "service_code": service.code,
                "total_price": str(rate.price)
            })
    
    return jsonify({"reference_id": req.get('request_reference'), "rates": rates})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=4010)
