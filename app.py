import os
import io
import zipfile
import base64
from flask import Flask, render_template, request

# pip install rembg
from rembg import remove

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_images():
    processed_images = []

    files = request.files.getlist('images')

    for file in files:
        img_data = file.read()
        
        # Background removal using rembg
        processed_data = remove(img_data)

        encoded_original = f"data:image/{file.mimetype.split('/')[1]};base64,{base64.b64encode(img_data).decode('utf-8')}"
        encoded_processed = f"data:image/png;base64,{base64.b64encode(processed_data).decode('utf-8')}"

        processed_images.append({
            'original': encoded_original,
            'processed': encoded_processed
        })

    return render_template('result.html', processed_images=processed_images)

if __name__ == "__main__":
    app.run(debug=True)
