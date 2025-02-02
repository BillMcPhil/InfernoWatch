from flask import Flask, jsonify, render_template, redirect, request, url_for
from flask_cors import CORS
import requests
import os
import math
import cv2
import numpy as np
import keras

API_KEY = os.environ["GOOGLE_API_KEY"]
SESSION_KEY = os.environ["SESSION_KEY"]
TILE_SIZE = 256
ZOOM = 15
app = Flask(__name__, template_folder="../client/public", static_folder="../client/src")
CORS(
    app, resources={r"/api/*": {"origins": "http://localhost:3000"}}
)  # Enable CORS for /api/*

model = None


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/api/test", methods=["GET"])
def api_test():
    return jsonify({"data": "HELLO"}), 200


def get_coords(address: str) -> tuple[float, float]:
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
        response = requests.get(url)
        y = response.json()
        return (
            y["results"][0]["geometry"]["location"]["lat"],
            y["results"][0]["geometry"]["location"]["lng"],
        )
    except:
        return "Request failed"


# Function to parse addresses to be properly formatted for map api
def parse_address(address: str) -> str:
    parsed_address = address.replace(" ", "+")
    return parsed_address


def lat_long_to_point(lat: float, long: float) -> list[int]:
    sinY = math.sin((lat * math.pi) / 180)
    mercatorY = math.log((1 + sinY) / (1 - sinY)) / 2
    return [
        TILE_SIZE * (long / 360 + 0.5),
        TILE_SIZE * (0.5 - mercatorY / (2 * math.pi)),
    ]


def lat_long_to_tile(lat: float, long: float, zoom: int) -> list[int]:
    point = lat_long_to_point(lat, long)
    scale = 2**ZOOM
    return [
        math.floor((point[0] * scale) / TILE_SIZE),
        math.floor((point[1] * scale) / TILE_SIZE),
    ]


def get_image(tile_coords: list[int]):
    url = f"https://tile.googleapis.com/v1/2dtiles/{ZOOM}/{tile_coords[0]}/{tile_coords[1]}?session={SESSION_KEY}&key={API_KEY}"
    resp = requests.get(url, stream=True).raw
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def predict(tile_coords: list[int], model):
    size = 5
    output_array = np.zeros((size, size))

    # Collect all images
    images = []
    coords_list = []

    for i in range(size):
        for j in range(size):
            cords = [tile_coords[0] + i, tile_coords[1] + j]
            coords_list.append(cords)
            img = get_image(cords)
            img = cv2.resize(img, (32, 32))  # Resize to match training data
            img = img / 255.0  # Normalize
            images.append(img)

    # Convert to numpy batch (batch_size, height, width, channels)
    images = np.array(images)
    images = np.expand_dims(
        images, axis=-1
    )  # Ensure correct shape for grayscale images

    # Perform batch prediction
    predictions = model.predict(images)

    # Convert predictions to binary classes
    predicted_classes = (predictions[:, 0] > 0.5).astype(int)

    # Fill output array and print positive predictions
    for idx, (i, j) in enumerate([(i, j) for i in range(size) for j in range(size)]):
        output_array[i, j] = predicted_classes[idx]
        if predicted_classes[idx] == 1:
            print(coords_list[idx])

    return output_array


# Define class labels (modify according to your dataset)
class_labels = ["nowildfire", "wildfire"]  # Assuming class names are folder names


@app.route("/predict", methods=["GET"])
def get_array():
    address = request.args.get("address")

    if not address:
        return jsonify({"error": "Address parameter is required"}), 400

    cords = get_coords(address)
    tile_coords = lat_long_to_tile(cords[0], cords[1], 15)

    prediction = predict(tile_coords, model)

    return jsonify({"address": address, "array": prediction.tolist()})


if __name__ == "__main__":
    model = keras.models.load_model("./server/model.keras")

    # cords = get_coords("92 Vanier Way, NS")
    cords = [50.16901564478449, -120.49729423675838]
    cords = [51.33364, -62.42947]
    cords = [51.29047, -62.56176]
    cords = [38.22651891110837, -120.64442835296504]
    crods = [39.50397623168039, -121.11008536095846]
    tile_coords = lat_long_to_tile(cords[0], cords[1],15)

    prediction = predict(tile_coords,model)
    print(prediction)

    # app.run(debug=True, port=8080)
