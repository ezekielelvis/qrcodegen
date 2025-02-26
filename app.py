# app.py
from flask import Flask, render_template, request, send_file, jsonify
import qrcode
from io import BytesIO
import base64
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Get form data
    data = request.form.get('data', 'https://example.com')
    box_size = int(request.form.get('box_size', 10))
    border = int(request.form.get('border', 4))
    fill_color = request.form.get('fill_color', '#000000')
    back_color = request.form.get('back_color', '#FFFFFF')
    error_correction = request.form.get('error_correction', 'H')
    
    # Map error correction level
    error_levels = {
        'L': qrcode.constants.ERROR_CORRECT_L,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'H': qrcode.constants.ERROR_CORRECT_H
    }
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_levels.get(error_correction),
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    # Save to BytesIO
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    # Convert to base64 for displaying in browser
    img_str = base64.b64encode(img_io.getvalue()).decode('utf-8')
    
    return jsonify({
        'image': f'data:image/png;base64,{img_str}',
        'success': True
    })

@app.route('/download', methods=['POST'])
def download():
    # Get form data
    data = request.form.get('data', 'https://example.com')
    box_size = int(request.form.get('box_size', 10))
    border = int(request.form.get('border', 4))
    fill_color = request.form.get('fill_color', '#000000')
    back_color = request.form.get('back_color', '#FFFFFF')
    error_correction = request.form.get('error_correction', 'H')
    
    # Map error correction level
    error_levels = {
        'L': qrcode.constants.ERROR_CORRECT_L,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'H': qrcode.constants.ERROR_CORRECT_H
    }
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_levels.get(error_correction),
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    # Save to BytesIO
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png', 
                    download_name='qrcode.png', as_attachment=True)

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Create the index.html file
    with open('templates/index.html', 'w') as f:
        f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Code Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .range-container {
            display: flex;
            align-items: center;
        }
        .range-container input[type="range"] {
            flex: 1;
        }
        .range-value {
            width: 40px;
            text-align: center;
            margin-left: 10px;
        }
        .color-inputs {
            display: flex;
            gap: 10px;
        }
        .color-input-group {
            flex: 1;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 15px;
            cursor: pointer;
            border-radius: 4px;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        .button-group {
            margin-top: 20px;
            text-align: center;
        }
        .button-group button {
            margin: 0 5px;
        }
        #download-btn {
            background-color: #2196F3;
        }
        #download-btn:hover {
            background-color: #0b7dda;
        }
        .qr-code-container {
            margin-top: 30px;
            text-align: center;
        }
        #qrcode {
            max-width: 100%;
            height: auto;
            margin: 0 auto;
            display: block;
            border: 1px solid #ddd;
            padding: 10px;
            background-color: white;
        }
        .error {
            color: red;
            text-align: center;
            margin-top: 10px;
        }
        .radio-group {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
        }
        .radio-option {
            margin-right: 10px;
        }
        @media (max-width: 600px) {
            .color-inputs {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>QR Code Generator</h1>
        
        <form id="qr-form">
            <div class="form-group">
                <label for="data">Text or URL:</label>
                <input type="text" id="data" name="data" value="https://example.com" required>
            </div>
            
            <div class="form-group">
                <label for="box-size">Box Size:</label>
                <div class="range-container">
                    <input type="range" id="box-size" name="box_size" min="1" max="20" value="10" oninput="updateBoxSizeValue(this.value)">
                    <span id="box-size-value" class="range-value">10</span>
                </div>
            </div>
            
            <div class="form-group">
                <label for="border">Border Size:</label>
                <div class="range-container">
                    <input type="range" id="border" name="border" min="0" max="10" value="4" oninput="updateBorderValue(this.value)">
                    <span id="border-value" class="range-value">4</span>
                </div>
            </div>
            
            <div class="form-group">
                <label>Error Correction Level:</label>
                <div class="radio-group">
                    <div class="radio-option">
                        <input type="radio" id="error-l" name="error_correction" value="L">
                        <label for="error-l">L (7%)</label>
                    </div>
                    <div class="radio-option">
                        <input type="radio" id="error-m" name="error_correction" value="M">
                        <label for="error-m">M (15%)</label>
                    </div>
                    <div class="radio-option">
                        <input type="radio" id="error-q" name="error_correction" value="Q">
                        <label for="error-q">Q (25%)</label>
                    </div>
                    <div class="radio-option">
                        <input type="radio" id="error-h" name="error_correction" value="H" checked>
                        <label for="error-h">H (30%)</label>
                    </div>
                </div>
            </div>
            
            <div class="form-group">
                <label>Colors:</label>
                <div class="color-inputs">
                    <div class="color-input-group">
                        <label for="fill-color">QR Color:</label>
                        <input type="color" id="fill-color" name="fill_color" value="#000000">
                    </div>
                    <div class="color-input-group">
                        <label for="back-color">Background Color:</label>
                        <input type="color" id="back-color" name="back_color" value="#FFFFFF">
                    </div>
                </div>
            </div>
            
            <div class="button-group">
                <button type="button" id="generate-btn">Generate QR Code</button>
                <button type="button" id="download-btn">Download QR Code</button>
            </div>
        </form>
        
        <div class="qr-code-container">
            <img id="qrcode" src="" alt="QR Code will appear here" style="display: none;">
            <p class="error" id="error-message"></p>
        </div>
    </div>

    <script>
        // Update displayed values for sliders
        function updateBoxSizeValue(val) {
            document.getElementById('box-size-value').textContent = val;
        }
        
        function updateBorderValue(val) {
            document.getElementById('border-value').textContent = val;
        }
        
        // Generate QR code
        document.getElementById('generate-btn').addEventListener('click', function() {
            generateQRCode();
        });
        
        // Download QR code
        document.getElementById('download-btn').addEventListener('click', function() {
            const form = document.getElementById('qr-form');
            const formData = new FormData(form);
            
            // Submit form to download endpoint
            const downloadForm = document.createElement('form');
            downloadForm.method = 'POST';
            downloadForm.action = '/download';
            
            for (const [key, value] of formData.entries()) {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = key;
                input.value = value;
                downloadForm.appendChild(input);
            }
            
            document.body.appendChild(downloadForm);
            downloadForm.submit();
            document.body.removeChild(downloadForm);
        });
        
        // Generate QR code on page load
        window.onload = function() {
            generateQRCode();
            
            // Also generate on input changes
            const inputs = document.querySelectorAll('input');
            inputs.forEach(input => {
                input.addEventListener('change', function() {
                    generateQRCode();
                });
            });
            
            // For text input, generate as you type
            document.getElementById('data').addEventListener('input', function() {
                generateQRCode();
            });
        };
        
        function generateQRCode() {
            const form = document.getElementById('qr-form');
            const formData = new FormData(form);
            const errorMsg = document.getElementById('error-message');
            
            fetch('/generate', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const qrImage = document.getElementById('qrcode');
                    qrImage.src = data.image;
                    qrImage.style.display = 'block';
                    errorMsg.style.display = 'none';
                } else {
                    errorMsg.textContent = data.error || 'An error occurred';
                    errorMsg.style.display = 'block';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                errorMsg.textContent = 'Failed to generate QR code';
                errorMsg.style.display = 'block';
            });
        }
    </script>
</body>
</html>
        ''')
    
    app.run(debug=True)