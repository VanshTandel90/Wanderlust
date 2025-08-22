import pandas as pd
from sklearn.linear_model import LinearRegression
import http.server
import socketserver
import json
import requests

OPENCAGE_API_KEY = "a43c2bbb84b14395a2c95c7ade397be8"
OPENCAGE_URL = "https://api.opencagedata.com/geocode/v1/json"

# --- Model Training ---
try:
    df = pd.read_csv('Airbnb_India_Top_500.csv')
    X = df[['location/lat', 'location/lng']]
    y = df['pricing/rate/amount']
    # No train/test split needed here, as the model is fully trained on the entire dataset
    model = LinearRegression()
    model.fit(X, y)
    print("Model trained successfully on the entire dataset.")
except FileNotFoundError:
    print("Error: 'Airbnb_India_Top_500.csv' not found. Please place it in the same directory.")
    exit()

def geocode_location(location):
    """Converts a location string into latitude and longitude using OpenCage API."""
    try:
        params = {
            'q': location,
            'key': OPENCAGE_API_KEY,
            'countrycode': 'in'  # Restrict searches to India
        }
        response = requests.get(OPENCAGE_URL, params=params)
        data = response.json()
        if data and data['results']:
            geometry = data['results'][0]['geometry']
            return geometry['lat'], geometry['lng']
        return None, None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None, None

class PricePredictionHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/predict-price':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            location = data.get('location')
            country = data.get('country')

            # Set CORS headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

            if not location or not country:
                self.wfile.write(json.dumps({'error': 'Location and country are required'}).encode('utf-8'))
                return

            if country.lower() != 'india':
                self.wfile.write(json.dumps({'error': 'Prediction is only available for India.'}).encode('utf-8'))
                return

            lat, lng = geocode_location(location)

            if lat is None or lng is None:
                self.wfile.write(json.dumps({'error': 'Could not geocode the provided location. Please be more specific.'}).encode('utf-8'))
                return
            
            predicted_price = model.predict([[lat, lng]])
            
            self.wfile.write(json.dumps({'predicted_price': predicted_price[0]}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server(port=8001):
    with socketserver.TCPServer(("", port), PricePredictionHandler) as httpd:
        print(f"Python server running at http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")

if __name__ == '__main__':
    run_server()
