from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import os
from pathlib import Path

app = Flask(__name__)

# Constants
BASE_URL = "https://raw.githubusercontent.com/BetterSEQTA/BetterSEQTA-Themes/main/store/backgrounds"
BACKGROUNDS_FILE = "../store/backgrounds.json"

def load_existing_data():
    if os.path.exists(BACKGROUNDS_FILE):
        with open(BACKGROUNDS_FILE, 'r') as f:
            return json.load(f)
    return {"backgrounds": []}

def save_data(data):
    with open(BACKGROUNDS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_image_files():
    directory = "../store/backgrounds/images/full"
    files = []
    for f in sorted(os.listdir(directory)):
        if f.startswith('image-') and f.endswith('.webp'):
            files.append(f)
    return files

@app.route('/')
def index():
    data = load_existing_data()
    image_files = get_image_files()
    # Get existing categories
    categories = set()
    for bg in data['backgrounds']:
        categories.add(bg['category'])
    
    return render_template('index.html', 
                         images=image_files,
                         categories=sorted(categories),
                         existing_data=data)

@app.route('/save', methods=['POST'])
def save():
    data = request.json
    save_data(data)
    return jsonify({"status": "success"})

@app.route('/backgrounds/images/<path:filename>')
def serve_image(filename):
    # Split the path to get the directory (thumb/full) and actual filename
    directory, image = os.path.split(filename)
    base_path = Path("../store/backgrounds/images").resolve()
    return send_from_directory(base_path / directory, image)

if __name__ == '__main__':
    app.run(debug=True)