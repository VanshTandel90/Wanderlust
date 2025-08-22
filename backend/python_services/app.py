import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import NearestNeighbors
import http.server
import socketserver
import json
import requests

# --- Global Variables & Setup ---
OPENCAGE_API_KEY = "a43c2bbb84b14395a2c95c7ade397be8"
OPENCAGE_URL = "https://api.opencagedata.com/geocode/v1/json"

# --- Train Price Prediction Model on Startup ---
try:
    df = pd.read_csv('Airbnb_India_Top_500.csv')
    price_model_X = df[['location/lat', 'location/lng']]
    price_model_y = df['pricing/rate/amount']
    price_model = LinearRegression()
    price_model.fit(price_model_X, price_model_y)
    print("Price prediction model trained successfully.")
except FileNotFoundError:
    print("Error: 'Airbnb_India_Top_500.csv' not found for price prediction.")
    price_model = None

# --- Geocoding Function ---
def geocode_location(location):
    """Converts a location string into latitude and longitude."""
    try:
        params = {'q': location, 'key': OPENCAGE_API_KEY, 'limit': 1}
        response = requests.get(OPENCAGE_URL, params=params)
        data = response.json()
        if data and data['results']:
            geometry = data['results'][0]['geometry']
            return geometry['lat'], geometry['lng']
        return None, None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None, None

# --- Main Request Handler ---
class APIHandler(http.server.BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        # --- Endpoint Routing ---
        if self.path == '/predict-price':
            self.handle_price_prediction(data)
        elif self.path == '/nearby':
            self.handle_nearby_recommendations(data)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def handle_price_prediction(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self._send_cors_headers()
        self.end_headers()
        
        if price_model is None:
            self.wfile.write(json.dumps({'error': 'Price prediction model is not available.'}).encode('utf-8'))
            return

        location = data.get('location')
        if not location:
            self.wfile.write(json.dumps({'error': 'Location is required.'}).encode('utf-8'))
            return
            
        lat, lng = geocode_location(location)
        if lat is None or lng is None:
            self.wfile.write(json.dumps({'error': 'Could not geocode the provided location.'}).encode('utf-8'))
            return
            
        predicted_price = price_model.predict([[lat, lng]])
        self.wfile.write(json.dumps({'predicted_price': predicted_price[0]}).encode('utf-8'))

    def handle_nearby_recommendations(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self._send_cors_headers()
        self.end_headers()

        user_location = data.get('user_location')
        listings = data.get('listings')

        if not user_location or not listings:
            self.wfile.write(json.dumps({'error': 'User location and listings are required.'}).encode('utf-8'))
            return

        user_lat, user_lng = geocode_location(user_location)
        if user_lat is None or user_lng is None:
            self.wfile.write(json.dumps({'error': f'Could not geocode user location: {user_location}'}).encode('utf-8'))
            return

        listing_coords = []
        geocoded_listings = []
        for listing in listings:
            full_address = f"{listing.get('location', '')}, {listing.get('country', '')}"
            lat, lng = geocode_location(full_address)
            if lat is not None and lng is not None:
                listing_coords.append([lat, lng])
                geocoded_listings.append(listing)

        if not listing_coords:
            self.wfile.write(json.dumps({'error': 'Could not geocode any listings.'}).encode('utf-8'))
            return
        
        n_neighbors = min(3, len(listing_coords))
        knn = NearestNeighbors(n_neighbors=n_neighbors, algorithm='ball_tree')
        knn.fit(listing_coords)
        
        distances, indices = knn.kneighbors([[user_lat, user_lng]])
        
        recommended = [geocoded_listings[i] for i in indices[0]]
        self.wfile.write(json.dumps({'nearby_listings': recommended}).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

def run_server(port=8001):
    with socketserver.TCPServer(("", port), APIHandler) as httpd:
        print(f"Python microservice running at http://localhost:{port}")
        httpd.serve_forever()

if __name__ == '__main__':
    run_server()