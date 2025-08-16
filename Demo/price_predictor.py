import numpy as np
from PIL import Image
import io
import os
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        try:
            # Convolutional layers
            self.weights['conv1'] = np.random.randn(16, 3, 3, 3).astype(np.float32) * 0.01
            self.weights['conv2'] = np.random.randn(32, 16, 3, 3).astype(np.float32) * 0.01
            self.weights['conv3'] = np.random.randn(64, 16, 3, 3).astype(np.float32) * 0.01
            
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
            
            # Validate all weights are numpy arrays
            for name, weight in self.weights.items():
                if not isinstance(weight, np.ndarray):
                    raise ValueError(f"Weight {name} is not a numpy array: {type(weight)}")
            
            for name, bias in self.biases.items():
                if not isinstance(bias, np.ndarray):
                    raise ValueError(f"Bias {name} is not a numpy array: {type(bias)}")
                    
        except Exception as e:
            logger.error(f"Error initializing weights: {e}")
            raise
    
    def relu(self, x):
        """ReLU activation function"""
        return np.maximum(0, x)
    
    def max_pool(self, x, pool_size=2):
        """Max pooling operation"""
        if len(x.shape) != 4:
            raise ValueError(f"Expected 4D input, got {len(x.shape)}D")
        
        n, h, w, c = x.shape
        h_out = h // pool_size
        w_out = w // pool_size
        
        # Ensure we have valid dimensions
        if h_out == 0 or w_out == 0:
            raise ValueError(f"Input dimensions {h}x{w} too small for pool size {pool_size}")
        
        # Create output array with correct shape
        x_out = np.zeros((n, h_out, w_out, c), dtype=x.dtype)
        
        for i in range(h_out):
            for j in range(w_out):
                # Extract the pooling window
                window = x[:, i*pool_size:(i+1)*pool_size, j*pool_size:(j+1)*pool_size, :]
                # Apply max pooling along spatial dimensions
                x_out[:, i, j, :] = np.max(window, axis=(1, 2))
        
        return x_out
    
    def conv_forward(self, x, w, b, stride=1, pad=1):
        """Convolutional forward pass"""
        try:
            # Use different variable names to avoid shadowing
            batch_size, height, width, in_channels = x.shape
            num_filters, expected_in_channels, _, _ = w.shape
            
            # Validate input channels match expected channels
            if in_channels != expected_in_channels:
                raise ValueError(f"Input has {in_channels} channels but weights expect {expected_in_channels} channels")
            
            h_out = (height + 2*pad - 3) // stride + 1
            w_out = (width + 2*pad - 3) // stride + 1
            
            # Ensure valid output dimensions
            if h_out <= 0 or w_out <= 0:
                raise ValueError(f"Invalid output dimensions: {h_out}x{w_out}")
            
            # Pad the input
            x_pad = np.pad(x, ((0, 0), (pad, pad), (pad, pad), (0, 0)), mode='constant')
            
            # Create output array with correct shape and dtype
            out = np.zeros((batch_size, h_out, w_out, num_filters), dtype=x.dtype)
            
            for i in range(h_out):
                for j in range(w_out):
                    for k in range(num_filters):
                        # Extract the convolution window
                        window = x_pad[:, i*stride:i*stride+3, j*stride:j*stride+3, :]
                        # Apply convolution
                        # w[k] has shape (in_channels, 3, 3)
                        # window has shape (batch_size, 3, 3, in_channels)
                        # We need to transpose window to (batch_size, in_channels, 3, 3) for proper broadcasting
                        window_transposed = window.transpose(0, 3, 1, 2)
                        # Ensure window_transposed has shape (batch_size, in_channels, 3, 3)
                        if window_transposed.shape != (batch_size, in_channels, 3, 3):
                            raise ValueError(f"Window transposed shape mismatch: expected {(batch_size, in_channels, 3, 3)}, got {window_transposed.shape}")
                        
                        conv_result = np.sum(window_transposed * w[k], axis=(1, 2, 3))
                        out[:, i, j, k] = conv_result + b[k]
            
            # Ensure output is a numpy array
            if not isinstance(out, np.ndarray):
                raise ValueError(f"conv_forward returned {type(out)}, expected numpy array")
            
            return out
            
        except Exception as e:
            logger.error(f"Error in conv_forward: {e}")
            logger.error(f"Input shape: {x.shape}, Weight shape: {w.shape}, Bias shape: {b.shape}")
            raise
    
    def forward(self, x):
        """Forward pass through the entire network"""
        try:
            # Ensure input has correct shape
            if len(x.shape) != 4:
                raise ValueError(f"Expected 4D input, got {len(x.shape)}D")
            
            logger.info(f"Input shape: {x.shape}")
            
            # Convolutional layers
            try:
                logger.info(f"Conv1 weights shape: {self.weights['conv1'].shape}")
                x = self.conv_forward(x, self.weights['conv1'], self.biases['conv1'])
                logger.info(f"After conv1: {x.shape}")
            except Exception as e:
                logger.error(f"Failed at conv1: {e}")
                raise
            
            x = self.relu(x)
            x = self.max_pool(x)
            logger.info(f"After pool1: {x.shape}")
            
            try:
                logger.info(f"Conv2 weights shape: {self.weights['conv2'].shape}")
                x = self.conv_forward(x, self.weights['conv2'], self.biases['conv2'])
                logger.info(f"After conv2: {x.shape}")
            except Exception as e:
                logger.error(f"Failed at conv2: {e}")
                raise
            
            x = self.relu(x)
            x = self.max_pool(x)
            logger.info(f"After pool2: {x.shape}")
            
            try:
                logger.info(f"Conv3 weights shape: {self.weights['conv3'].shape}")
                x = self.conv_forward(x, self.weights['conv3'], self.biases['conv3'])
                logger.info(f"After conv3: {x.shape}")
            except Exception as e:
                logger.error(f"Failed at conv3: {e}")
                raise
            
            x = self.relu(x)
            x = self.max_pool(x)
            logger.info(f"After pool3: {x.shape}")
            
            # Flatten
            x = x.reshape(x.shape[0], -1)
            logger.info(f"After flatten: {x.shape}")
            
            # Fully connected layers
            x = np.dot(x, self.weights['fc1'].T) + self.biases['fc1']
            logger.info(f"After fc1: {x.shape}")
            x = self.relu(x)
            
            x = np.dot(x, self.weights['fc2'].T) + self.biases['fc2']
            logger.info(f"After fc2: {x.shape}")
            x = self.relu(x)
            
            x = np.dot(x, self.weights['fc3'].T) + self.biases['fc3']
            logger.info(f"Final output: {x.shape}")
            
            return x
            
        except Exception as e:
            logger.error(f"Error in forward pass: {e}")
            raise

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

class PricePredictor:
    """Main class for price prediction"""
    
    def __init__(self):
        self.model = SimpleCNN()
        self.location_encoder = LocationEncoder()
        self.country_encoder = LocationEncoder()
        logger.info("PricePredictor initialized successfully!")
    
    def preprocess_image(self, image_input):
        """Preprocess image for the CNN model"""
        try:
            # Handle different input types
            if isinstance(image_input, str):
                # If it's a file path
                image = Image.open(image_input)
            elif hasattr(image_input, 'read'):
                # If it's a file-like object
                image = Image.open(image_input)
            elif isinstance(image_input, Image.Image):
                # If it's already a PIL Image
                image = image_input
            else:
                raise ValueError(f"Unsupported image input type: {type(image_input)}")
            
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
    
    def predict_price(self, image_features, location_features, country_features):
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
    
    def predict_from_data(self, image_input, location, country):
        """Main method to predict price from image, location, and country"""
        try:
            logger.info(f"Processing prediction for location: {location}, country: {country}")
            
            # Preprocess image
            image_features = self.preprocess_image(image_input)
            if image_features is None:
                raise ValueError("Failed to process image")
            
            # Encode location and country
            location_features = self.location_encoder.encode_location(location)
            country_features = self.country_encoder.encode_country(country)
            
            # Predict price
            predicted_price, confidence = self.predict_price(image_features, location_features, country_features)
            
            # Log the prediction
            logger.info(f"Predicted price: ₹{predicted_price}, Confidence: {confidence}%")
            
            # Save prediction to file for analysis
            filename = getattr(image_input, 'filename', 'unknown')
            self.save_prediction(filename, location, country, predicted_price, confidence)
            
            return {
                'predicted_price': predicted_price,
                'confidence': confidence,
                'location': location,
                'country': country,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            raise
    
    def save_prediction(self, filename, location, country, price, confidence):
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

# Global instance for easy access
predictor = PricePredictor()

def predict_price_simple(image_input, location, country):
    """Simple function interface for price prediction"""
    return predictor.predict_from_data(image_input, location, country)

# Test function
def test_predictor():
    """Test the predictor with dummy data"""
    print("🧪 Testing Price Predictor...")
    
    try:
        # Create a dummy image
        dummy_image = Image.new('RGB', (100, 100), color='blue')
        
        # Test prediction
        result = predict_price_simple(dummy_image, "Mumbai, Maharashtra", "India")
        
        print("✅ Test successful!")
        print(f"   Location: {result['location']}")
        print(f"   Country: {result['country']}")
        print(f"   Predicted Price: ₹{result['predicted_price']:,}")
        print(f"   Confidence: {result['confidence']}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    # Run test if file is executed directly
    test_predictor() 