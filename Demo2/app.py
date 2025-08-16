import http.server
import socketserver
import urllib.parse
import json
import os
import cgi
from price_predictor import predict_price_simple
import base64
from io import BytesIO

class PricePredictionHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode())
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/predict':
            try:
                # Parse form data
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )
                
                # Get form data
                location = form.getvalue('location', '')
                country = form.getvalue('country', '')
                
                # Handle image file
                if 'image' in form:
                    image_file = form['image']
                    if image_file.filename:
                        # Read image data
                        image_data = image_file.file.read()
                        image_file.file.close()
                        
                        # Create BytesIO object for PIL
                        image_io = BytesIO(image_data)
                        
                        # Make prediction
                        result = predict_price_simple(image_io, location, country)
                        
                        # Send JSON response
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(json.dumps(result).encode())
                        return
                
                # If no image or error
                error_response = {'error': 'No image provided or invalid image'}
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode())
                
            except Exception as e:
                error_response = {'error': str(e)}
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()

# HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wanderlust - Price Prediction (No Flask)</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #fe424d 0%, #ff6b6b 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }

        .form-container {
            padding: 40px;
        }

        .form-group {
            margin-bottom: 25px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #333;
            font-size: 1.1rem;
        }

        .form-group input {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }

        .form-group input:focus {
            outline: none;
            border-color: #fe424d;
        }

        .image-preview {
            margin-top: 15px;
            text-align: center;
        }

        .image-preview img {
            max-width: 300px;
            max-height: 200px;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            display: none;
        }

        .submit-btn {
            background: linear-gradient(135deg, #fe424d 0%, #ff6b6b 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 1.1rem;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.2s ease;
            width: 100%;
            font-weight: bold;
        }

        .submit-btn:hover {
            transform: translateY(-2px);
        }

        .submit-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .result-container {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            text-align: center;
            display: none;
        }

        .predicted-price {
            font-size: 2.5rem;
            font-weight: bold;
            color: #fe424d;
            margin: 15px 0;
        }

        .confidence {
            font-size: 1.1rem;
            color: #666;
        }

        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #fe424d;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .error {
            background: #ffe6e6;
            color: #d63031;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            display: none;
        }

        .info-box {
            background: #e3f2fd;
            color: #1976d2;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧭 Wanderlust</h1>
            <p>AI-Powered Price Prediction (No Flask)</p>
        </div>

        <div class="form-container">
            <div class="info-box">
                <strong>🚀 Working Demo:</strong> This version works without Flask using Python's built-in HTTP server!
            </div>

            <form id="pricePredictionForm" enctype="multipart/form-data">
                <div class="form-group">
                    <label for="image">Upload Property Image</label>
                    <input type="file" id="image" name="image" accept="image/*" required>
                    <div class="image-preview">
                        <img id="imagePreview" alt="Image preview">
                    </div>
                </div>

                <div class="form-group">
                    <label for="location">Location</label>
                    <input type="text" id="location" name="location" placeholder="e.g., Kolak, Valsad" required>
                </div>

                <div class="form-group">
                    <label for="country">Country</label>
                    <input type="text" id="country" name="country" placeholder="e.g., India" required>
                </div>

                <button type="submit" class="submit-btn" id="submitBtn">
                    🚀 Predict Price
                </button>
            </form>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Analyzing your property with AI...</p>
            </div>

            <div class="result-container" id="resultContainer">
                <h3>Predicted Price</h3>
                <div class="predicted-price" id="predictedPrice">₹0</div>
                <div class="confidence" id="confidence">Confidence: 0%</div>
                <div class="details" id="details"></div>
            </div>

            <div class="error" id="error"></div>
        </div>
    </div>

    <script>
        // Image preview functionality
        document.getElementById('image').addEventListener('change', function(e) {
            const file = e.target.files[0];
            const preview = document.getElementById('imagePreview');
            
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });

        // Form submission
        document.getElementById('pricePredictionForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = document.getElementById('submitBtn');
            const loading = document.getElementById('loading');
            const resultContainer = document.getElementById('resultContainer');
            const error = document.getElementById('error');
            
            // Hide previous results and errors
            resultContainer.style.display = 'none';
            error.style.display = 'none';
            
            // Show loading
            loading.style.display = 'block';
            submitBtn.disabled = true;
            
            try {
                const formData = new FormData();
                formData.append('image', document.getElementById('image').files[0]);
                formData.append('location', document.getElementById('location').value);
                formData.append('country', document.getElementById('country').value);
                
                const response = await fetch('/predict', {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const result = await response.json();
                
                if (result.error) {
                    throw new Error(result.error);
                }
                
                // Display results
                document.getElementById('predictedPrice').textContent = `₹${result.predicted_price.toLocaleString('en-IN')}`;
                document.getElementById('confidence').textContent = `Confidence: ${result.confidence}%`;
                document.getElementById('details').innerHTML = `
                    <p><strong>Location:</strong> ${result.location}</p>
                    <p><strong>Country:</strong> ${result.country}</p>
                `;
                resultContainer.style.display = 'block';
                
            } catch (err) {
                console.error('Error:', err);
                error.textContent = 'Error: ' + err.message;
                error.style.display = 'block';
            } finally {
                loading.style.display = 'none';
                submitBtn.disabled = false;
            }
        });
    </script>
</body>
</html>
'''

def run_server(port=8000):
    """Run the HTTP server"""
    with socketserver.TCPServer(("", port), PricePredictionHandler) as httpd:
        print(f"🚀 Server running at http://localhost:{port}")
        print(f"📱 Open your browser and go to: http://localhost:{port}")
        print(f"⏹️  Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == '__main__':
    run_server() 