import requests
from flask import current_app

class OpenRouteService:
    def __init__(self, api_key=None):
        self.api_key = api_key or current_app.config.get('ORS_API_KEY')
        self.base_url = 'https://api.openrouteservice.org/v2'
    
    def calculate_distance(self, from_coords, to_coords):
        url = f"{self.base_url}/directions/driving-car"
        headers = {'Authorization': self.api_key}
        body = {
            'coordinates': [
                [from_coords['lon'], from_coords['lat']],
                [to_coords['lon'], to_coords['lat']]
            ]
        }
        try:
            response = requests.post(url, json=body, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get('routes'):
                route = data['routes'][0]['summary']
                return {
                    'distance_km': round(route['distance'] / 1000, 2),
                    'duration_minutes': round(route['duration'] / 60, 1)
                }
        except:
            pass
        return None
