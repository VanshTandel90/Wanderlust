from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
from PIL import Image
import io
import base64
import os
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global variables for the model
model = None
location_encoder = None
country_encoder = None
scaler = None

class SimpleCNN:
    """A simple CNN model for price prediction"""
    
    def __init__(self):
        self.weights = {}
        self.biases = {}
        self.initialize_weights()
    
    def initialize_weights(self):
        """Initialize random weights for the CNN layers"""
        # Convolutional layers
        self.weights['conv1'] = np.random.randn(16, 3, 3, 3) * 0.01
        self.weights['conv2'] = np.random.randn(32, 16, 3, 3) * 0.01
        self.weights['conv3'] = np.random.randn(64, 32, 3, 3) * 0.01
        
        # Fully connected layers
        self.weights['fc1'] = np.random.randn(128, 64 * 8 * 8) * 0.01
        self.weights['fc2'] = np.random.randn(64, 128) * 0.01
        self.weights['fc3'] = np.random.randn(1, 64) * 0.01
        
        # Biases
        self.biases['conv1'] = np.zeros(16)
        self.biases['conv2'] = np.zeros(32)
        self.biases['conv3'] = np.zeros(64)
        self.biases['fc1'] = np.zeros(128)
        self.biases['fc2'] = np.zeros(64)
        self.biases['fc3'] = np.zeros(1)
    
    def relu(self, x):
        """ReLU activation function"""
        return np.maximum(0, x)
    
    def max_pool(self, x, pool_size=2):
        """Max pooling operation"""
        h, w = x.shape[1:3]
        h_out = h // pool_size
        w_out = w // pool_size
        x_out = np.zeros((x.shape[0], h_out, w_out, x.shape[3]))
        
        for i in range(h_out):
            for j in range(w_out):
                x_out[:, i, j, :] = np.max(x[:, i*pool_size:(i+1)*pool_size, 
                                               j*pool_size:(j+1)*pool_size, :], axis=(1, 2))
        return x_out
    
    def conv_forward(self, x, w, b, stride=1, pad=1):
        """Convolutional forward pass"""
        n, h, w, c = x.shape
        f, _, _, _ = w.shape
        
        h_out = (h + 2*pad - f) // stride + 1
        w_out = (w + 2*pad - f) // stride + 1
        
        # Pad the input
        x_pad = np.pad(x, ((0, 0), (pad, pad), (pad, pad), (0, 0)), mode='constant')
        
        out = np.zeros((n, h_out, w_out, f))
        
        for i in range(h_out):
            for j in range(w_out):
                for k in range(f):
                    out[:, i, j, k] = np.sum(
                        x_pad[:, i*stride:i*stride+f, j*stride:j*stride+f, :] * w[k],
                        axis=(1, 2, 3)
                    ) + b[k]
        
        return out
    
    def forward(self, x):
        """Forward pass through the entire network"""
        # Convolutional layers
        x = self.conv_forward(x, self.weights['conv1'], self.biases['conv1'])
        x = self.relu(x)
        x = self.max_pool(x)
        
        x = self.conv_forward(x, self.weights['conv2'], self.biases['conv2'])
        x = self.relu(x)
        x = self.max_pool(x)
        
        x = self.conv_forward(x, self.weights['conv3'], self.biases['conv3'])
        x = self.relu(x)
        x = self.max_pool(x)
        
        # Flatten
        x = x.reshape(x.shape[0], -1)
        
        # Fully connected layers
        x = np.dot(x, self.weights['fc1'].T) + self.biases['fc1']
        x = self.relu(x)
        
        x = np.dot(x, self.weights['fc2'].T) + self.biases['fc2']
        x = self.relu(x)
        
        x = np.dot(x, self.weights['fc3'].T) + self.biases['fc3']
        
        return x

class LocationEncoder:
    """Simple location encoding based on text features"""
    
    def __init__(self):
        self.location_features = {}
        self.country_features = {}
    
    def encode_location(self, location):
        """Encode location text to numerical features"""
        location = location.lower()
        
        # Simple feature extraction based on text characteristics
        features = []
        
        # Length of location name
        features.append(len(location))
        
        # Number of words
        features.append(len(location.split()))
        
        # Presence of common location indicators
        indicators = ['city', 'town', 'village', 'beach', 'mountain', 'valley', 'resort']
        for indicator in indicators:
            features.append(1.0 if indicator in location else 0.0)
        
        # Character frequency features
        vowels = 'aeiou'
        features.append(sum(1 for char in location if char in vowels))
        features.append(len(location) - sum(1 for char in location if char in vowels))
        
        return np.array(features)
    
    def encode_country(self, country):
        """Encode country text to numerical features"""
        country = country.lower()
        
        features = []
        
        # Length of country name
        features.append(len(country))
        
        # Number of words
        features.append(len(country.split()))
        
        # Character frequency
        vowels = 'aeiou'
        features.append(sum(1 for char in country if char in vowels))
        features.append(len(country) - sum(1 for char in country if char in vowels))
        
        return np.array(features)

def preprocess_image(image_file):
    """Preprocess uploaded image for the CNN model"""
    try:
        # Read image
        image = Image.open(image_file.stream)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to 64x64 (smaller size for demo)
        image = image.resize((64, 64))
        
        # Convert to numpy array and normalize
        image_array = np.array(image) / 255.0
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
        
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        return None

def predict_price(image_features, location_features, country_features):
    """Predict price using the CNN model and location features"""
    try:
        # Combine all features
        combined_features = np.concatenate([
            image_features.flatten(),
            location_features,
            country_features
        ])
        
        # Simple price prediction logic (this would be replaced by actual model training)
        # For demo purposes, we'll use a combination of image features and location
        
        # Base price from image features (simulate luxury detection)
        image_luxury_score = np.mean(image_features) * 1000
        
        # Location multiplier (simulate location-based pricing)
        location_multiplier = 1.0 + (np.sum(location_features) * 0.1)
        
        # Country multiplier (simulate country-based pricing)
        country_multiplier = 1.0 + (np.sum(country_features) * 0.05)
        
        # Calculate predicted price
        base_price = 2000  # Base price in INR
        predicted_price = (base_price + image_luxury_score) * location_multiplier * country_multiplier
        
        # Add some randomness to simulate real prediction
        noise = np.random.normal(0, 0.1)
        predicted_price *= (1 + noise)
        
        # Ensure price is reasonable
        predicted_price = max(500, min(50000, predicted_price))
        
        # Calculate confidence (simulate model confidence)
        confidence = min(95, max(60, 80 + np.random.normal(0, 10)))
        
        return int(predicted_price), round(confidence, 1)
        
    except Exception as e:
        logger.error(f"Error in price prediction: {e}")
        return 2000, 50.0

@app.route('/predict-price', methods=['POST'])
def predict_price_endpoint():
    """Endpoint for price prediction"""
    try:
        # Check if image is provided
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image_file = request.files['image']
        location = request.form.get('location', '')
        country = request.form.get('country', '')
        
        if not location or not country:
            return jsonify({'error': 'Location and country are required'}), 400
        
        logger.info(f"Processing prediction for location: {location}, country: {country}")
        
        # Preprocess image
        image_features = preprocess_image(image_file)
        if image_features is None:
            return jsonify({'error': 'Failed to process image'}), 400
        
        # Encode location and country
        location_features = location_encoder.encode_location(location)
        country_features = location_encoder.encode_country(country)
        
        # Predict price
        predicted_price, confidence = predict_price(image_features, location_features, country_features)
        
        # Log the prediction
        logger.info(f"Predicted price: ₹{predicted_price}, Confidence: {confidence}%")
        
        # Save prediction to file for analysis
        save_prediction(image_file.filename, location, country, predicted_price, confidence)
        
        return jsonify({
            'predicted_price': predicted_price,
            'confidence': confidence,
            'location': location,
            'country': country,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in prediction endpoint: {e}")
        return jsonify({'error': str(e)}), 500

def save_prediction(filename, location, country, price, confidence):
    """Save prediction results to a file for analysis"""
    try:
        prediction_data = {
            'filename': filename,
            'location': location,
            'country': country,
            'predicted_price': price,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        }
        
        # Create predictions directory if it doesn't exist
        os.makedirs('predictions', exist_ok=True)
        
        # Save to JSON file
        with open(f'predictions/prediction_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
            json.dump(prediction_data, f, indent=2)
            
    except Exception as e:
        logger.error(f"Error saving prediction: {e}")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

def initialize_model():
    """Initialize the CNN model and encoders"""
    global model, location_encoder, country_encoder
    
    try:
        logger.info("Initializing CNN model...")
        model = SimpleCNN()
        
        logger.info("Initializing location encoder...")
        location_encoder = LocationEncoder()
        country_encoder = LocationEncoder()
        
        logger.info("Model initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"Error initializing model: {e}")
        raise

if __name__ == '__main__':
    try:
        # Initialize the model
        initialize_model()
        
        # Run the Flask app
        logger.info("Starting Flask server...")
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        exit(1) 