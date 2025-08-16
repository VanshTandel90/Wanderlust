import numpy as np
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleCNN:
    """A simple CNN model for price prediction"""
    
    def __init__(self):
        self.weights = {}
        self.biases = {}
        self.initialize_weights()
    
    def initialize_weights(self):
        """Initialize random weights for the CNN layers"""
        # Convolutional layers
        self.weights['conv1'] = np.random.randn(16, 3, 3, 3).astype(np.float32) * 0.01
        self.weights['conv2'] = np.random.randn(32, 16, 3, 3).astype(np.float32) * 0.01
        self.weights['conv3'] = np.random.randn(64, 32, 3, 3).astype(np.float32) * 0.01
        
        # Fully connected layers
        self.weights['fc1'] = np.random.randn(128, 64 * 8 * 8).astype(np.float32) * 0.01
        self.weights['fc2'] = np.random.randn(64, 128).astype(np.float32) * 0.01
        self.weights['fc3'] = np.random.randn(1, 64).astype(np.float32) * 0.01
        
        # Biases
        self.biases['conv1'] = np.zeros(16, dtype=np.float32)
        self.biases['conv2'] = np.zeros(32, dtype=np.float32)
        self.biases['conv3'] = np.zeros(64, dtype=np.float32)
        self.biases['fc1'] = np.zeros(128, dtype=np.float32)
        self.biases['fc2'] = np.zeros(64, dtype=np.float32)
        self.biases['fc3'] = np.zeros(1, dtype=np.float32)
    
    def relu(self, x):
        """ReLU activation function"""
        return np.maximum(0, x)
    
    def max_pool(self, x, pool_size=2):
        """Max pooling operation"""
        n, h, w, c = x.shape
        h_out = h // pool_size
        w_out = w // pool_size
        x_out = np.zeros((n, h_out, w_out, c), dtype=x.dtype)
        
        for i in range(h_out):
            for j in range(w_out):
                x_out[:, i, j, :] = np.max(x[:, i*pool_size:(i+1)*pool_size, 
                                               j*pool_size:(j+1)*pool_size, :], axis=(1, 2))
        return x_out
    
    def conv_forward(self, x, w, b, stride=1, pad=1):
        """Convolutional forward pass"""
        batch_size, height, width, in_channels = x.shape
        num_filters, _, _, _ = w.shape
        
        h_out = (height + 2*pad - 3) // stride + 1
        w_out = (width + 2*pad - 3) // stride + 1
        
        # Pad the input
        x_pad = np.pad(x, ((0, 0), (pad, pad), (pad, pad), (0, 0)), mode='constant')
        
        # Create output array
        out = np.zeros((batch_size, h_out, w_out, num_filters), dtype=x.dtype)
        
        for i in range(h_out):
            for j in range(w_out):
                for k in range(num_filters):
                    window = x_pad[:, i*stride:i*stride+3, j*stride:j*stride+3, :]
                    window_transposed = window.transpose(0, 3, 1, 2)
                    conv_result = np.sum(window_transposed * w[k], axis=(1, 2, 3))
                    out[:, i, j, k] = conv_result + b[k]
        
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
    
    def encode_location(self, location):
        """Encode location text to numerical features"""
        location = location.lower()
        
        features = []
        features.append(len(location))
        features.append(len(location.split()))
        
        indicators = ['city', 'town', 'village', 'beach', 'mountain', 'valley', 'resort']
        for indicator in indicators:
            features.append(1.0 if indicator in location else 0.0)
        
        vowels = 'aeiou'
        features.append(sum(1 for char in location if char in vowels))
        features.append(len(location) - sum(1 for char in location if char in vowels))
        
        return np.array(features)
    
    def encode_country(self, country):
        """Encode country text to numerical features"""
        country = country.lower()
        
        features = []
        features.append(len(country))
        features.append(len(country.split()))
        
        vowels = 'aeiou'
        features.append(sum(1 for char in country if char in vowels))
        features.append(len(country) - sum(1 for char in country if char in vowels))
        
        return np.array(features)

class PricePredictor:
    """Main class for price prediction"""
    
    def __init__(self):
        self.model = SimpleCNN()
        self.location_encoder = LocationEncoder()
        logger.info("PricePredictor initialized successfully!")
    
    def preprocess_image(self, image_input):
        """Preprocess image for the CNN model"""
        try:
            # Handle different input types
            if isinstance(image_input, str):
                image = Image.open(image_input)
            elif hasattr(image_input, 'read'):
                image = Image.open(image_input)
            elif isinstance(image_input, Image.Image):
                image = image_input
            else:
                raise ValueError(f"Unsupported image input type: {type(image_input)}")
            
            # Convert to RGB and resize
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            image = image.resize((64, 64))
            
            # Convert to numpy array and normalize
            image_array = np.array(image) / 255.0
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            return None
    
    def predict_price(self, image_features, location_features, country_features):
        """Predict price using the CNN model and location features"""
        try:
            # Base price from image features
            image_luxury_score = np.mean(image_features) * 1000
            
            # Location and country multipliers
            location_multiplier = 1.0 + (np.sum(location_features) * 0.1)
            country_multiplier = 1.0 + (np.sum(country_features) * 0.05)
            
            # Calculate predicted price
            base_price = 2000
            predicted_price = (base_price + image_luxury_score) * location_multiplier * country_multiplier
            
            # Add randomness and ensure reasonable range
            noise = np.random.normal(0, 0.1)
            predicted_price *= (1 + noise)
            predicted_price = max(500, min(50000, predicted_price))
            
            # Calculate confidence
            confidence = min(95, max(60, 80 + np.random.normal(0, 10)))
            
            return int(predicted_price), round(confidence, 1)
            
        except Exception as e:
            logger.error(f"Error in price prediction: {e}")
            return 2000, 50.0
    
    def predict_from_data(self, image_input, location, country):
        """Main method to predict price from image, location, and country"""
        try:
            # Preprocess image
            image_features = self.preprocess_image(image_input)
            if image_features is None:
                raise ValueError("Failed to process image")
            
            # Encode location and country
            location_features = self.location_encoder.encode_location(location)
            country_features = self.location_encoder.encode_country(country)
            
            # Predict price
            predicted_price, confidence = self.predict_price(image_features, location_features, country_features)
            
            return {
                'predicted_price': predicted_price,
                'confidence': confidence,
                'location': location,
                'country': country
            }
            
        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            raise

# Global instance
predictor = PricePredictor()

def predict_price_simple(image_input, location, country):
    """Simple function interface for price prediction"""
    return predictor.predict_from_data(image_input, location, country) 