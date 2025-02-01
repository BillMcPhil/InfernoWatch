from flask import Flask, jsonify, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_cors import CORS
import json
import requests
import secrets

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

API_KEY = "" #API key goes here
app = Flask(__name__, template_folder="../client/public", static_folder="../client/src")
foo = secrets.token_urlsafe(16)
app.secret_key = foo
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # Enable CORS for /api/*

bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

class AddressForm(FlaskForm):
    address = StringField("Please type in your address :)", validators=[DataRequired(), Length(0, 60)])
    submit = SubmitField("Submit")

@app.route("/", methods=["GET", "POST"])
def index():
    form = AddressForm()
    message = ""
    if form.validate_on_submit():
        address = form.address.data
        parsed_address = parse_address(address)
        coords = get_coords(parsed_address)
        print(coords)
    return render_template("index.html", form=form)
    


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

if __name__ == "__main__":
    app.run(debug=True, port=8080)
