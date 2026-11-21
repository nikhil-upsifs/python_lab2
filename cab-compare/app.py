"""Cab price comparator — compares Uber, Ola and Rapido fares.

Run:  python app.py  ->  open http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, jsonify

import fare_engine
import geo

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/api/compare", methods=["POST"])
def compare_api():
    payload = request.get_json(silent=True) or {}
    pickup = (payload.get("pickup") or "").strip()
    drop = (payload.get("drop") or "").strip()
    traffic = payload.get("traffic_kmph")
    if not pickup or not drop:
        return jsonify({"error": "Please provide both pickup and drop locations."}), 400
    try:
        trip = geo.resolve_trip(pickup, drop)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    result = fare_engine.compare(trip["distance_km"], traffic)
    result["pickup"] = {"lat": trip["pickup"][0], "lon": trip["pickup"][1]}
    result["drop"] = {"lat": trip["drop"][0], "lon": trip["drop"][1]}
    result["route_duration_min"] = round(trip["duration_min"])
    result["pickup_text"] = pickup
    result["drop_text"] = drop
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
