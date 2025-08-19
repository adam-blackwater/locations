import math
from typing import List, Dict
from octopus_exercise.api.models import Location
from geopy.distance import geodesic


def location_wintin_distance(
    locationOne: Location,
    locationTwo: Location,
    distance: int = 10
) -> bool:
    point1 = (locationOne.coordinates.lat, locationOne.coordinates.lon)
    point2 = (locationTwo.coordinates.lat, locationTwo.coordinates.lon)
    
    distance_m = geodesic(point1, point2).meters
    return distance_m <= distance

def get_closest(lat: float , lon: float, locations: List[Location]):
    def distance_from_reference(loc: Location) -> float:
        return haversine(
            lat,
            lon,
            loc.coordinates.lat,
            loc.coordinates.lon
        )
    return sorted(locations, key=distance_from_reference)

def assign_location_a_distance(lat, lon, locations: List[Location]):
    distances: List[Dict[Location, float]] = []
    for loc in locations:
        d = haversine(
            lat, lon,
            loc.coordinates.lat, loc.coordinates.lon
        )
    distances.append({"location": loc, "distance": d})

def haversine(lat1, lon1, lat2, lon2):
    # Earth radius in kilometers (use 3958.8 for miles)
    R = 6371.0  
    
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c
