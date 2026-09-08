```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timezone

app = Flask(__name__)

# Allow your website to request GPS data
CORS(app)

latest_location = {
    "latitude": None,
    "longitude": None,
    "timestamp": None
}


@app.route("/")
def home():
    return "Location server is running!"


@app.route("/location", methods=["POST"])
def receive_location():
    global latest_location

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude is None or longitude is None:
        return jsonify({
            "error": "Missing latitude or longitude"
        }), 400

    latest_location = {
        "latitude": latitude,
        "longitude": longitude,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    print("New location:", latest_location)

    return jsonify({
        "success": True,
        "location": latest_location
    })


@app.route("/location", methods=["GET"])
def get_location():
    return jsonify(latest_location)


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
```
