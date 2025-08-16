# 🧭 Wanderlust - AI Price Prediction Demo (No Flask)

This demo showcases an AI-powered price prediction system for property listings using a custom CNN model built from scratch. **No Flask server required!**

## 🚀 Features

- **Custom CNN Model**: Built from scratch using NumPy (no pre-trained models)
- **Image Analysis**: Processes property images to extract visual features
- **Location Encoding**: Converts location and country text to numerical features
- **Price Prediction**: Combines image and location features to predict listing prices
- **No Server Required**: Works entirely locally with Python scripts
- **Beautiful UI**: Modern, responsive HTML interface
- **Easy Integration**: Simple Python modules that can be imported anywhere

## 🛠️ Architecture

### Frontend (HTML/JavaScript)
- Image upload with preview
- Location and country input forms
- Form data export to JSON
- Demo examples and instructions
- Responsive design with modern styling

### Backend (Pure Python)
- **SimpleCNN Class**: Custom CNN implementation with:
  - 3 convolutional layers (16, 32, 64 filters)
  - Max pooling operations
  - 3 fully connected layers
  - ReLU activation functions
- **LocationEncoder**: Text feature extraction for location and country
- **PricePredictor**: Main class that orchestrates the prediction process
- **Image Preprocessing**: Resize to 64x64, normalize, convert to RGB

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Modern web browser

## 🚀 Installation & Setup

### 1. Install Python Dependencies
```bash
cd Demo
pip install -r requirements.txt
```

### 2. Test the Setup
```bash
python test_demo.py
```

### 3. Open the HTML Demo
Open `index.html` in your web browser.

## 🎯 How to Use

### Method 1: Web Interface + Python Script
1. **Open HTML**: Open `index.html` in your browser
2. **Fill Form**: Upload image, enter location and country
3. **Download Data**: Click "📥 Download Form Data" to get JSON file
4. **Save Image**: Save your image file to the Demo folder
5. **Run Prediction**: Use the provided command in terminal
6. **View Results**: See prediction in terminal output

### Method 2: Direct Python Usage
```python
from price_predictor import predict_price_simple
from PIL import Image

# Create or load an image
image = Image.open("your_property.jpg")

# Predict price
result = predict_price_simple(image, "Mumbai, Maharashtra", "India")
print(f"Predicted Price: ₹{result['predicted_price']:,}")
print(f"Confidence: {result['confidence']}%")
```

### Method 3: Command Line
```bash
python run_prediction.py "house.jpg" "Mumbai, Maharashtra" "India"
```

## 🔬 How It Works

### CNN Model Architecture
```
Input Image (64x64x3)
    ↓
Conv1 (16 filters) + ReLU + MaxPool
    ↓
Conv2 (32 filters) + ReLU + MaxPool  
    ↓
Conv3 (64 filters) + ReLU + MaxPool
    ↓
Flatten
    ↓
FC1 (128 neurons) + ReLU
    ↓
FC2 (64 neurons) + ReLU
    ↓
FC3 (1 neuron) → Price Output
```

### Feature Engineering
- **Image Features**: Extracted through CNN layers
- **Location Features**: 
  - Text length and word count
  - Presence of location indicators (city, beach, mountain, etc.)
  - Character frequency analysis
- **Country Features**: Similar text-based encoding

### Price Prediction Algorithm
```
Base Price + Image Luxury Score × Location Multiplier × Country Multiplier
```

## 📁 File Structure

```
Demo/
├── index.html              # Frontend interface (no Flask needed)
├── price_predictor.py      # Main CNN model and prediction logic
├── run_prediction.py       # Script to run predictions from command line
├── test_demo.py           # Test script to verify everything works
├── requirements.txt        # Python dependencies (no Flask)
├── README.md              # This file
└── predictions/           # Generated prediction logs
```

## 🎨 Customization

### Modify CNN Architecture
Edit the `SimpleCNN` class in `price_predictor.py`:
- Change filter sizes and counts
- Add/remove layers
- Modify activation functions

### Adjust Price Prediction Logic
Modify the `predict_price()` method in `PricePredictor`:
- Change base price
- Adjust multipliers
- Add more sophisticated algorithms

### Enhance Location Encoding
Improve the `LocationEncoder` class:
- Add more text features
- Use word embeddings
- Include geographic coordinates

## 🧪 Testing

### Run All Tests
```bash
python test_demo.py
```

### Test Individual Components
```bash
# Test CNN model
python -c "from price_predictor import SimpleCNN; model = SimpleCNN(); print('✅ CNN works!')"

# Test location encoder
python -c "from price_predictor import LocationEncoder; encoder = LocationEncoder(); print('✅ Encoder works!')"

# Test complete predictor
python price_predictor.py
```

## 🔮 Future Enhancements

- **Real Model Training**: Collect data and train actual weights
- **Advanced Features**: Add property type, amenities, seasonality
- **Model Persistence**: Save and load trained models
- **Batch Processing**: Handle multiple predictions
- **Performance Metrics**: Accuracy, RMSE, MAE calculations
- **Integration**: Easy integration into main Wanderlust app

## 🚫 Why No Flask?

This demo is designed to be:
- **Lightweight**: No server dependencies
- **Portable**: Works on any machine with Python
- **Integratable**: Easy to import into existing projects
- **Educational**: Clear separation of concerns
- **Fast**: No network overhead

## 🐛 Troubleshooting

### Common Issues
1. **Import errors**: Ensure you're in the Demo directory
2. **Image processing errors**: Check image format and size
3. **Memory issues**: Large images may cause problems

### Debug Mode
Run individual components to isolate issues:
```bash
python -c "import price_predictor; print('Import successful')"
```

## 📝 License

This demo is part of the Wanderlust project. Feel free to modify and enhance for your own use.

## 🤝 Contributing

To improve this demo:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Note**: This is a demonstration implementation. For production use, you would need to:
- Train the model on real data
- Implement proper error handling
- Add security measures
- Optimize performance
- Add comprehensive testing

## 🎉 Quick Start Example

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Test everything works
python test_demo.py

# 3. Try a quick prediction
python -c "
from price_predictor import predict_price_simple
from PIL import Image
img = Image.new('RGB', (100, 100), 'blue')
result = predict_price_simple(img, 'Mumbai, Maharashtra', 'India')
print(f'Price: ₹{result[\"predicted_price\"]:,}')
"
``` 