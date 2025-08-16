#!/usr/bin/env python3
"""
Test script for the CNN model and location encoder
This script tests the basic functionality without running the Flask server
"""

import numpy as np
from price_prediction import SimpleCNN, LocationEncoder, preprocess_image
from PIL import Image
import io

def test_cnn_model():
    """Test the CNN model with random input"""
    print("🧪 Testing CNN Model...")
    
    # Create model
    model = SimpleCNN()
    print("✅ CNN model created successfully")
    
    # Create random test image (64x64x3)
    test_image = np.random.rand(1, 64, 64, 3)
    print(f"✅ Test image created: {test_image.shape}")
    
    # Test forward pass
    try:
        output = model.forward(test_image)
        print(f"✅ Forward pass successful: Output shape {output.shape}")
        print(f"   Predicted value: {output[0, 0]:.4f}")
    except Exception as e:
        print(f"❌ Forward pass failed: {e}")
        return False
    
    return True

def test_location_encoder():
    """Test the location encoder"""
    print("\n🧪 Testing Location Encoder...")
    
    # Create encoder
    encoder = LocationEncoder()
    print("✅ Location encoder created successfully")
    
    # Test location encoding
    test_location = "Kolak, Valsad"
    test_country = "India"
    
    try:
        location_features = encoder.encode_location(test_location)
        country_features = encoder.encode_country(test_country)
        
        print(f"✅ Location encoding successful:")
        print(f"   Location: '{test_location}' → {location_features}")
        print(f"   Country: '{test_country}' → {country_features}")
        
    except Exception as e:
        print(f"❌ Location encoding failed: {e}")
        return False
    
    return True

def test_image_preprocessing():
    """Test image preprocessing with a dummy image"""
    print("\n🧪 Testing Image Preprocessing...")
    
    try:
        # Create a dummy image file object
        dummy_image = Image.new('RGB', (100, 100), color='red')
        img_byte_arr = io.BytesIO()
        dummy_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        # Create a mock file object
        class MockFile:
            def __init__(self, data):
                self.stream = data
        
        mock_file = MockFile(img_byte_arr)
        
        # Test preprocessing
        processed = preprocess_image(mock_file)
        
        if processed is not None:
            print(f"✅ Image preprocessing successful: {processed.shape}")
            print(f"   Data range: {processed.min():.3f} to {processed.max():.3f}")
        else:
            print("❌ Image preprocessing failed")
            return False
            
    except Exception as e:
        print(f"❌ Image preprocessing failed: {e}")
        return False
    
    return True

def test_price_prediction_logic():
    """Test the price prediction logic"""
    print("\n🧪 Testing Price Prediction Logic...")
    
    try:
        # Mock features
        image_features = np.random.rand(1, 64, 64, 3)
        location_features = np.array([10, 2, 1, 0, 0, 0, 0, 4, 6])  # Example location features
        country_features = np.array([5, 1, 2, 3])  # Example country features
        
        # Import the prediction function
        from price_prediction import predict_price
        
        predicted_price, confidence = predict_price(image_features, location_features, country_features)
        
        print(f"✅ Price prediction successful:")
        print(f"   Predicted price: ₹{predicted_price:,}")
        print(f"   Confidence: {confidence}%")
        
        # Validate output
        if 500 <= predicted_price <= 50000 and 60 <= confidence <= 95:
            print("✅ Price and confidence within expected ranges")
        else:
            print("⚠️  Price or confidence outside expected ranges")
            
    except Exception as e:
        print(f"❌ Price prediction failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting Demo Tests...\n")
    
    tests = [
        ("CNN Model", test_cnn_model),
        ("Location Encoder", test_location_encoder),
        ("Image Preprocessing", test_image_preprocessing),
        ("Price Prediction", test_price_prediction_logic)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed\n")
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}\n")
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The demo is ready to run.")
        print("\n🚀 To run the demo:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Start backend: python price_prediction.py")
        print("   3. Open index.html in your browser")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 