"""Fare estimation engine for Uber, Ola and Rapido.

Uses publicly known fare structures (base fare, per-km, per-minute,
minimum fare) to estimate ride prices. Estimates are approximate and
do not replace live quotes from the platforms.
"""

import math
import random
from datetime import datetime

# Ride category -> platform-specific fare configs.
# fare = (base + km_min * dist_km + per_min * minutes) ; min_fare floor
# dist_per_min approximates average city speed (km/h) / 60
RIDE_TYPES = {
    "Bike": {
        "Uber": {"base": 10, "per_km": 5.5, "per_min": 0.8, "min_fare": 25, "name": "Uber Moto"},
        "Ola": {"base": 12, "per_km": 5.0, "per_min": 1.0, "min_fare": 30, "name": "Ola Bike"},
        "Rapido": {"base": 8, "per_km": 4.5, "per_min": 0.7, "min_fare": 20, "name": "Rapido Bike"},
    },
    "Auto": {
        "Uber": {"base": 30, "per_km": 12.0, "per_min": 1.0, "min_fare": 40, "name": "Uber Auto"},
        "Ola": {"base": 30, "per_km": 12.5, "per_min": 1.0, "min_fare": 45, "name": "Ola Auto"},
        "Rapido": {"base": 25, "per_km": 11.0, "per_min": 1.0, "min_fare": 35, "name": "Rapido Auto"},
    },
    "Cab Economy": {
        "Uber": {"base": 55, "per_km": 16.0, "per_min": 1.5, "min_fare": 80, "name": "Uber Go"},
        "Ola": {"base": 60, "per_km": 15.5, "per_min": 1.5, "min_fare": 85, "name": "Ola Mini"},
        "Rapido": {"base": 50, "per_km": 15.0, "per_min": 1.2, "min_fare": 75, "name": "Rapido Cab"},
    },
    "Cab Premium": {
        "Uber": {"base": 70, "per_km": 20.0, "per_min": 2.0, "min_fare": 110, "name": "Uber Premier"},
        "Ola": {"base": 75, "per_km": 19.5, "per_min": 2.0, "min_fare": 115, "name": "Ola Prime"},
        "Rapido": {"base": 65, "per_km": 18.5, "per_min": 1.8, "min_fare": 100, "name": "Rapido Cab XL"},
    },
    "SUV / XL": {
        "Uber": {"base": 90, "per_km": 24.0, "per_min": 2.5, "min_fare": 150, "name": "Uber XL"},
        "Ola": {"base": 95, "per_km": 23.5, "per_min": 2.5, "min_fare": 155, "name": "Ola Prime SUV"},
        "Rapido": {"base": 85, "per_km": 22.0, "per_min": 2.2, "min_fare": 140, "name": "Rapido SUV"},
    },
}


def _surge_multiplier(platform: str, dt: datetime) -> float:
    """Simple time-based surge model (peak hours + night charges)."""
    hour = dt.hour
    surge = 1.0
    # Morning / evening office peaks and late-night demand
    if 8 <= hour <= 11 or 17 <= hour <= 21:
        surge += 0.20
    if 23 <= hour or hour <= 4:
        surge += 0.30
    # Slight per-platform bias so numbers differ a little
    jitter = {"Uber": 0.02, "Ola": 0.01, "Rapido": -0.01}[platform]
    # small deterministic-ish wobble in [0, 0.05)
    wobble = random.uniform(0.0, 0.05)
    return round(surge + jitter + wobble, 2)


def estimate_fare(platform: str, cfg: dict, dist_km: float, surge: float, traffic: float) -> int:
    dist_km = max(dist_km, 0.0)
    minutes = (dist_km / max(traffic, 5.0)) * 60  # traffic = avg speed km/h
    raw = cfg["base"] + cfg["per_km"] * dist_km + cfg["per_min"] * minutes
    raw *= surge
    return max(int(round(raw / 5.0) * 5), cfg["min_fare"])  # round to nearest 5


def compare(dist_km: float, traffic_kmph: float | None = None, dt: datetime | None = None):
    """Return all platforms grouped by ride type, with cheapest flagged."""
    dt = dt or datetime.now()
    # avg speed: slow city traffic ~ 20-25 km/h in peak, ~30 otherwise
    if traffic_kmph is None:
        traffic_kmph = 18.0 if _surge_multiplier("Uber", dt) > 1.15 else 28.0

    cheapest = {}
    results = {}
    for ride_type, platforms in RIDE_TYPES.items():
        entries = []
        for platform, cfg in platforms.items():
            entry = {
                "platform": platform,
                "name": cfg["name"],
                "surge": _surge_multiplier(platform, dt) if cfg["per_km"] < 20 else _surge_multiplier(platform, dt),
            }
            entry["price"] = estimate_fare(platform, cfg, dist_km, entry["surge"], traffic_kmph)
            entries.append(entry)
        best = min(entries, key=lambda e: e["price"])
        cheapest.setdefault(ride_type, (best["platform"], best["price"]))
        for e in entries:
            e["cheapest"] = e["platform"] == best["platform"]
            e["eta_min"] = round(dist_km / traffic_kmph * 60) + random.randint(2, 6)
        results[ride_type] = entries

    overall = min(cheapest.values(), key=lambda x: x[1])
    return {
        "distance_km": round(dist_km, 2),
        "est_traffic_kmph": round(traffic_kmph, 1),
        "results": results,
        "best": {"ride_type": None, "platform": overall[0], "price": overall[1]},
    }


def obvious_cheapest_allowed_categories():
    """Categories where comparing platforms actually makes sense."""
    return list(RIDE_TYPES.keys())
