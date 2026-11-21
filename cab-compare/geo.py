"""Geocoding (pickup/drop -> coordinates) and road-distance estimation.

Uses free OpenStreetMap services:
- Nominatim for geocoding
- OSRM public router for road distance/duration (falls back to haversine)
"""

import math
import time
import urllib.parse
import urllib.request
import json

GEOCODE_CACHE: dict[str, tuple[float, float]] = {}

_UA = "CabCompareApp/1.0 (educational project)"


def _get_json(url: str, timeout: float = 10.0):
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def geocode(place: str) -> tuple[float, float]:
    """Return (lat, lon) for a place name, with in-memory caching."""
    place = place.strip()
    if not place:
        raise ValueError("Empty place name")
    if place.lower() in GEOCODE_CACHE:
        return GEOCODE_CACHE[place.lower()]

    url = (
        "https://nominatim.openstreetmap.org/search?"
        + urllib.parse.urlencode({"q": place + ", India", "format": "json", "limit": 1})
    )
    data = _get_json(url)
    if not data:
        raise ValueError(f"Could not find place: {place}")
    lat, lon = float(data[0]["lat"]), float(data[0]["lon"])
    GEOCODE_CACHE[place.lower()] = (lat, lon)
    return lat, lon


def haversine_km(p1, p2) -> float:
    lat1, lon1 = map(math.radians, p1)
    lat2, lon2 = map(math.radians, p2)
    a = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 6371.0 * 2 * math.asin(math.sqrt(a))


def route_distance_km(p1, p2) -> tuple[float, float]:
    """(distance_km, duration_min) via OSRM road routing; haversine fallback."""
    url = (
        f"https://router.project-osrm.org/route/v1/driving/"
        f"{p1[1]},{p1[0]};{p2[1]},{p2[0]}?overview=false"
    )
    try:
        data = _get_json(url, timeout=8.0)
        if data.get("code") == "Ok" and data["routes"]:
            r = data["routes"][0]
            return r["distance"] / 1000.0, r["duration"] / 60.0
    except Exception:
        pass
    straight = haversine_km(p1, p2)
    return straight * 1.35, straight * 1.35 / 28.0 * 60.0  # road-factor fallback


def resolve_trip(pickup: str, drop: str):
    p = geocode(pickup)
    d = geocode(drop)
    time.sleep(0.1)  # be polite to Nominatim usage policy
    dist, dur = route_distance_km(p, d)
    return {"pickup": p, "drop": d, "distance_km": dist, "duration_min": dur}
