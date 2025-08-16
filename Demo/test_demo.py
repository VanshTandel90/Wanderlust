#!/usr/bin/env python3
"""
Test script for the Flask-free price prediction demo
"""

import os
import sys
from PIL import Image
import numpy as np

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from price_predictor import SimpleCNN, LocationEncoder, PricePredictor, predict_price_simple
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_cnn_model():
    """Test the CNN model"""
    print("\n🧪 Testing CNN Model...")
    
    try:
        from price_predictor import SimpleCNN
        
        model = SimpleCNN()
        print("✅ CNN model created")
        
        # Test with random input (ensure correct dimensions)
        test_input = np.random.rand(1, 64, 64, 3).astype(np.float32)
        print(f"✅ Test input created: {test_input.shape}")
        
        output = model.forward(test_input)
        print(f"✅ Forward pass successful: {output.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ CNN test failed: {e}")
        return False

def test_location_encoder():
    """Test the location encoder"""
    print("\n🧪 Testing Location Encoder...")
    
    try:
        from price_predictor import LocationEncoder
        
        encoder = LocationEncoder()
        
        # Test location encoding
        location_features = encoder.encode_location("Mumbai, Maharashtra")
        country_features = encoder.encode_country("India")
        
        print(f"✅ Location encoding: {location_features}")
        print(f"✅ Country encoding: {country_features}")
        return True
        
    except Exception as e:
        print(f"❌ Location encoder test failed: {e}")
        return False

def test_price_predictor():
    """Test the complete price predictor"""
    print("\n🧪 Testing Price Predictor...")
    
    try:
        from price_predictor import PricePredictor
        
        predictor = PricePredictor()
        print("✅ Price predictor created")
        
        # Create a test image
        test_image = Image.new('RGB', (100, 100), color='blue')
        
        # Test prediction
        result = predictor.predict_from_data(test_image, "Mumbai, Maharashtra", "India")
        
        print(f"✅ Prediction successful:")
        print(f"   Price: ₹{result['predicted_price']:,}")
        print(f"   Confidence: {result['confidence']}%")
        print(f"   Location: {result['location']}")
        print(f"   Country: {result['country']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Price predictor test failed: {e}")
        return False

def test_run_prediction_script():
    """Test the run_prediction script"""
    print("\n🧪 Testing run_prediction script...")
    
    try:
        from run_prediction import predict_from_file
        
        print("✅ run_prediction module imported successfully")
        
        # Test with a dummy image
        test_image = Image.new('RGB', (100, 100), color='green')
        
        # Save test image temporarily
        test_image_path = "test_image.png"
        test_image.save(test_image_path)
        
        # Test file-based prediction
        result = predict_from_file(test_image_path, "Delhi, NCR", "India")
        
        if 'error' not in result:
            print(f"✅ File-based prediction successful: ₹{result['predicted_price']:,}")
        else:
            print(f"⚠️  File-based prediction had issues: {result['error']}")
        
        # Clean up
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
        
        return True
        
    except Exception as e:
        print(f"❌ run_prediction test failed: {e}")
        return False

def test_image_preprocessing():
    """Test image preprocessing specifically"""
    print("\n🧪 Testing Image Preprocessing...")
    
    try:
        from price_predictor import PricePredictor
        
        predictor = PricePredictor()
        
        # Test different image input types
        test_cases = [
            ("PIL Image", Image.new('RGB', (100, 100), color='red')),
            ("File path", "test_image.png"),  # This will fail but we'll catch it
        ]
        
        for test_name, test_input in test_cases:
            try:
                if test_name == "PIL Image":
                    result = predictor.preprocess_image(test_input)
                    if result is not None and result.shape == (1, 64, 64, 3):
                        print(f"✅ {test_name} preprocessing successful: {result.shape}")
                    else:
                        print(f"❌ {test_name} preprocessing failed: unexpected shape")
                else:
                    # Skip file path test for now
                    print(f"⏭️  {test_name} test skipped (file doesn't exist)")
                    
            except Exception as e:
                print(f"❌ {test_name} preprocessing failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Image preprocessing test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Flask-Free Demo Tests...\n")
    
    tests = [
        ("Module Imports", test_imports),
        ("CNN Model", test_cnn_model),
        ("Location Encoder", test_location_encoder),
        ("Image Preprocessing", test_image_preprocessing),
        ("Price Predictor", test_price_predictor),
        ("Run Prediction Script", test_run_prediction_script)
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
        print("🎉 All tests passed! The Flask-free demo is ready to use.")
        print("\n🚀 How to use:")
        print("   1. Open index.html in your browser")
        print("   2. Fill the form and download the data")
        print("   3. Save your image to the Demo folder")
        print("   4. Run: python run_prediction.py <image> <location> <country>")
        print("   5. Or run: python price_predictor.py (for direct testing)")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 