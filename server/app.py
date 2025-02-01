from flask import Flask, jsonify, render_template
from flask_cors import CORS
import json
import requests

API_KEY = #API key goes here
app = Flask(__name__, template_folder="../client/public", static_folder="../client/src")
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # Enable CORS for /api/*

@app.route("/")
def home():
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
    parsed_address = ""
    for char in address:
        if char == " ":
            parsed_address += "+"
        else:
            parsed_address += char
    return parsed_address

if __name__ == "__main__":
    app.run(debug=True, port=8080)
