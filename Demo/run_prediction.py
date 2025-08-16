#!/usr/bin/env python3
"""
Simple script to run price prediction without Flask
This script can be called from HTML or run directly
"""

import sys
import os
from PIL import Image

# Add current directory to path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from price_predictor import predict_price_simple

def predict_from_file(image_path, location, country):
    """Predict price from image file path"""
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            return {'error': f'Image file not found: {image_path}'}
        
        # Open image file
        with open(image_path, 'rb') as f:
            image = Image.open(f)
            image.load()  # Ensure image is loaded
        
        # Make prediction
        result = predict_price_simple(image, location, country)
        return result
        
    except Exception as e:
        return {'error': str(e)}

def main():
    """Main function for command line usage"""
    print("🧭 Wanderlust Price Prediction")
    print("=" * 40)
    
    if len(sys.argv) < 4:
        print("Usage: python run_prediction.py <image_path> <location> <country>")
        print("Example: python run_prediction.py house.jpg 'Mumbai, Maharashtra' 'India'")
        return
    
    image_path = sys.argv[1]
    location = sys.argv[2]
    country = sys.argv[3]
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file '{image_path}' not found")
        return
    
    print(f"📸 Image: {image_path}")
    print(f"📍 Location: {location}")
    print(f"🌍 Country: {country}")
    print("\n🚀 Processing...")
    
    try:
        result = predict_from_file(image_path, location, country)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
        else:
            print("\n✅ Prediction Complete!")
            print(f"💰 Predicted Price: ₹{result['predicted_price']:,}")
            print(f"🎯 Confidence: {result['confidence']}%")
            print(f"⏰ Timestamp: {result['timestamp']}")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main() 