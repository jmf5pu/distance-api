import math
from project.settings import GMAPS_GEOCODE_API_URL
from typing import Tuple, Dict
import requests

def get_geocode_api_results(params: Dict[str, str]):
    geocode_response = requests.get(
        GMAPS_GEOCODE_API_URL,
        params=params
    )
    return geocode_response.json()['results'][0]

def calculate_distance(start_lat: float, start_lng: float, end_lat: float, end_lng: float) -> float:
    """
    Calculates the distance between (start_lat, start_lng) and (end_lat, end_lng) coordinates
    using Haversine formula
    """
    EARTH_RADIUS = 6371

    for lat in [start_lat, end_lat]:
        assert -90 <= lat and lat <= 90, f"received invalid latitude: {lat}"

    for lng in [start_lng, end_lng]:
        assert -180 <= lng and lng <= 180, f"received invalid longitude: {lng}"

    dlat = math.radians(end_lat - start_lat)
    dlon = math.radians(end_lng - start_lng)
    a = (math.sin(dlat / 2) ** 2 + math.cos(math.radians(start_lat)) * math.cos(math.radians(end_lat)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = EARTH_RADIUS * c
    return distance

def get_coords_tuple(coords: str) -> Tuple[float, float]:
    """
    Converts a string containing two float values into a tuple of floats
    """
    return tuple(map(float, coords.split(',')))