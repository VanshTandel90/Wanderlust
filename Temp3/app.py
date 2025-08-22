import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import requests
import json
import os
from flask import Flask, request, jsonify, render_template_string
import pickle

# Constants for the OpenCage Geocoding API
OPENCAGE_API_KEY = "YOUR_OPENCAGE_API_KEY" # Replace with your actual API key
OPENCAGE_URL = "https://api.opencagedata.com/geocode/v1/json"

# File names for the model and scaler
MODEL_FILE = 'price_prediction_model.pkl'

app = Flask(__name__)

# Function to get longitude and latitude from a location string
def geocode_location(location):
    try:
        params = {
            'q': location,
            'key': OPENCAGE_API_KEY,
            'countrycode': 'in' # Only search in India
        }
        response = requests.get(OPENCAGE_URL, params=params)
        data = response.json()
        if data and data['results']:
            geometry = data['results'][0]['geometry']
            print(geometry['lat'])
            return geometry['lat'], geometry['lng']
        return None, None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None, None

# Function to train and save the model
def train_model():
    # Load data from the CSV file
    df = pd.read_csv('Airbnb_India_Top_500.csv')
    
    # Use only location lat/lng and price
    X = df[['location/lat', 'location/lng']].values
    y = df['pricing/rate/amount'].values
    
    # Create and train the linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Save the model
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(model, f)
    
    print("Model trained and saved successfully!")

# Train model when the application starts
if not os.path.exists(MODEL_FILE):
    train_model()

# Load the trained model
with open(MODEL_FILE, 'rb') as f:
    price_model = pickle.load(f)

# HTML template for the form
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Wanderlust Price Predictor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2rem; }
        form { display: flex; flex-direction: column; width: 300px; }
        label { margin-top: 1rem; }
        input { padding: 0.5rem; margin-top: 0.5rem; }
        button { padding: 0.75rem; margin-top: 1rem; background-color: #007BFF; color: white; border: none; cursor: pointer; }
        #result { margin-top: 2rem; font-size: 1.2rem; }
    </style>
</head>
<body>
    <h1>Predict Airbnb Price in India</h1>
    <form id="predictionForm">
        <label for="location">Location:</label>
        <input type="text" id="location" name="location" placeholder="e.g., Delhi, India" required>
        
        <label for="country">Country:</label>
        <input type="text" id="country" name="country" value="India" disabled>
        
        <button type="submit">Predict Price</button>
    </form>
    <div id="result"></div>

    <script>
        document.getElementById('predictionForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const location = document.getElementById('location').value;
            
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ location: location })
            });

            const result = await response.json();
            const resultDiv = document.getElementById('result');
            
            if (result.error) {
                resultDiv.innerHTML = `<p style="color: red;">Error: ${result.error}</p>`;
            } else {
                resultDiv.innerHTML = `<p>Predicted Price: ₹${result.predicted_price.toFixed(2)}</p>`;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    location = data.get('location')
    
    if not location:
        return jsonify({'error': 'Location is required'}), 400
    
    # Geocode the location to get latitude and longitude
    lat, lng = geocode_location(location)
    
    if lat is None or lng is None:
        return jsonify({'error': 'Could not geocode the provided location. Please be more specific.'}), 400
        
    # Use the trained model to predict the price
    predicted_price = price_model.predict([[lat, lng]])
    
    return jsonify({'predicted_price': predicted_price[0]})

if __name__ == '__main__':
    # You must get an API key from OpenCage Geocoding to use this feature.
    # The current one will fail without a valid key.
    # This is a good way to convert location string to lat/long in a simple way
    app.run(port=5000)