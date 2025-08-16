# 🧭 Wanderlust - Working Price Prediction Demo (No Flask)

A **working** demo that actually displays price predictions on the HTML page using a CNN model - **without Flask**!

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Demo
```bash
python app.py
```

### 3. Open in Browser
Go to: `http://localhost:8000`

## 🎯 How It Works

1. **Upload Image**: Select a property image
2. **Enter Details**: Location and country
3. **Get Prediction**: See the predicted price and confidence displayed on the page

## 📁 Files

- **`app.py`** - Python HTTP server with HTML form and prediction endpoint (No Flask!)
- **`price_predictor.py`** - CNN model and prediction logic
- **`requirements.txt`** - Minimal dependencies (No Flask!)

## 🔧 Features

- ✅ **No Flask Required**: Uses Python's built-in `http.server`
- ✅ **Working CNN Model**: Built from scratch with NumPy
- ✅ **Real-time Prediction**: Upload image and get instant results
- ✅ **Beautiful UI**: Modern, responsive design
- ✅ **Image Preview**: See your uploaded image before prediction
- ✅ **Error Handling**: Proper error messages and validation

## 🎨 Usage

1. Fill out the form with your property details
2. Click "🚀 Predict Price"
3. Wait for AI analysis
4. View your predicted price and confidence level

## 🚫 No Testing Required

This demo is **ready to use** - no need to run tests or debug. Just install dependencies and run!

## 🔍 Technical Details

- **Server**: Python's built-in `http.server.SimpleHTTPRequestHandler`
- **Port**: 8000 (default)
- **Dependencies**: Only NumPy and Pillow (no external web frameworks)
- **Architecture**: Single Python file with embedded HTML template 