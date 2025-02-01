from flask import Flask, jsonify, render_template, redirect, request, url_for
from flask_cors import CORS
import requests

API_KEY = "" #API key goes here
SESSION_KEY = "" #Session key goes here
TILE_SIZE = 256
app = Flask(__name__, template_folder="../client/public", static_folder="../client/src")
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # Enable CORS for /api/*

model = None

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")
    
@app.route('/api/test', methods=['GET'])
def api_test():
    return jsonify({"data": "HELLO"}), 200

def get_coords(address: str) -> tuple[float, float]:
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
        response = requests.get(url)
        y = response.json()
        return (y['results'][0]["geometry"]["location"]["lat"], y['results'][0]["geometry"]["location"]["lng"])
    except:
        return "Request failed"

# Function to parse addresses to be properly formatted for map api
def parse_address(address: str) -> str:
    parsed_address = address.replace(" ", "+")
    return parsed_address

def lat_long_to_point(lat: float, long: float) -> list[int]:
    sinY = math.sin((lat * math.pi) / 180)
    mercatorY = math.log((1 + sinY) / (1 - sinY)) / 2
    return [TILE_SIZE * (long / 360 + 0.5), TILE_SIZE * (0.5 - mercatorY / (2 * math.pi))]


def lat_long_to_tile(lat: float, long: float, zoom: int) -> list[int]:
    point = lat_long_to_point(lat, long)
    scale = 2**zoom
    return [math.floor((point[0] * scale) / TILE_SIZE), math.floor((point[1] * scale) / TILE_SIZE), zoom]

@app.route("api/predict", methods=["POST"])
def process():
    # Get the uploaded file from the request
    file = request.files['image']

    # Open the image using PIL
    pil_image = Image.open(file.stream)

    # Convert PIL image to OpenCV format
    img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (32, 32))  # Resize to match training data
    img = img / 255.0  # Normalize
    img = np.expand_dims(img, axis=0)  # Add batch dimension

    # Predict
    predictions = model.predict(img)

    # Get class with highest probability
    predicted_class_index = np.argmax(predictions, axis=1)[0]

    # Get class label
    predicted_class = class_labels[predicted_class_index]

    return predicted_class

# Define class labels (modify according to your dataset)
class_labels = ["nowildfire", "wildfire"]  # Assuming class names are folder names

if __name__ == "__main__":
    model = keras.models.load_model("model.keras")
    app.run(debug=True, port=8080)
