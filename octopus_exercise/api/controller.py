from typing import List, Optional

from sqlalchemy.orm import Session

from octopus_exercise.api.builders import (
    build_detailed_location_response,
    build_locations_response,
)
from octopus_exercise.api.models import LocationDetailedResponse, LocationsResponse, Location
from octopus_exercise.db.crud import find_all_locations, find_specific_location
from octopus_exercise.db.models import LocationTableModel
from octopus_exercise.utils.geolocation import get_closest


def get_all_locations(
    db: Session,
    country: Optional[str] = None,
    operator: Optional[str] = None,
    order_by_last_updated: Optional[bool] = None,
    decending: Optional[bool] = None,
    lat: Optional[int] = None,
    lon: Optional[int] = None,
) -> LocationsResponse:
    locations_from_db: List[LocationTableModel] = find_all_locations(
        db,
        country,
        operator,
        order_by_last_updated,
        decending,
    )
    locations_response: LocationsResponse = build_locations_response(locations_from_db)
    if lat and lon:
        # TODO add better guarding again bad input
        sorted_locations: List[Location] = get_closest(lat, lon, locations_response.locations)
        locations_response.locations = sorted_locations
        return locations_response
    return locations_response

def get_detailed_location(db: Session, operator_reference: str) -> LocationDetailedResponse:
    location_from_db: List[LocationTableModel] = find_specific_location(db, operator_reference)
    detailed_response: LocationDetailedResponse = build_detailed_location_response(location_from_db)
    return detailed_response
