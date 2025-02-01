from flask import Flask, jsonify, render_template
from flask_cors import CORS

API_KEY = #API KEY GOES HERE
app = Flask(__name__, template_folder="../client/public", static_folder="../client/src")
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # Enable CORS for /api/*

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/api/test', methods=['GET'])
def api_test():
    return jsonify({"data": "HELLO"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=8080)
