import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import requests
import json

# You must get a valid API key from OpenCage for geocoding.
# Replace 'YOUR_OPENCAGE_API_KEY' with your actual key.
OPENCAGE_API_KEY = "a43c2bbb84b14395a2c95c7ade397be8"
OPENCAGE_URL = "https://api.opencagedata.com/geocode/v1/json"

def geocode_location(location):
    """Converts a location string into latitude and longitude using OpenCage API."""
    try:
        params = {
            'q': location,
            'key': OPENCAGE_API_KEY,
            'countrycode': 'in'  # Restrict searches to India as per the dataset
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

def run_prediction_test():
    """Trains a linear regression model and evaluates it using multiple metrics."""
    # Load data from the CSV file
    try:
        df = pd.read_csv('Airbnb_India_Top_500.csv')
    except FileNotFoundError:
        print("Error: 'Airbnb_India_Top_500.csv' not found. Please ensure it is in the same directory.")
        return

    # Select features (X) and target (y)
    X = df[['location/lat', 'location/lng']]
    y = df['pricing/rate/amount']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=32)

    # Instantiate and train the linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Get a location from the user for a sample prediction
    user_location = input("Enter a location in India to predict the price (e.g., 'New Delhi'): ")
    
    # Geocode the user's location
    lat, lng = geocode_location(user_location)
    
    if lat is not None and lng is not None:
        # Create a DataFrame for the single prediction
        sample_input = pd.DataFrame([[lat, lng]], columns=['location/lat', 'location/lng'])
        
        # Predict the price for the sample input
        predicted_price = model.predict(sample_input)
        print(f"\nPredicted price for '{user_location}': ₹{predicted_price[0]:.2f}")
    else:
        print("\nCould not geocode the location. Please try again with a more specific location name.")

if __name__ == "__main__":
    run_prediction_test()
