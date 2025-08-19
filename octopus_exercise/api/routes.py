from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from octopus_exercise.api.controller import get_all_locations, get_detailed_location
from octopus_exercise.db.session import get_db

from .models import LocationDetailedResponse, LocationsResponse

router = APIRouter(prefix="/api")

@router.get("/locations")
def read_location(
    db: Session = Depends(get_db),
    country: Optional[str] = Query(None, description="Filter by country"),
    operator: Optional[str]  = Query(None, description="Filter by operator"),
    order: Optional[str] = Query(None, regex="^last_updated_(asc|desc)$"),
    lat: Optional[int] = Query(None, description="latitude"),
    lon: Optional[int] = Query(None, description="longitude"),
) -> LocationsResponse:
    order_by_last_updated = False
    descending = True

    if order is not None:
        order_by_last_updated = True
        descending = order.endswith("desc")

    return get_all_locations(
        db,
        country,
        operator,
        order_by_last_updated,
        descending,
        lat,
        lon,
    )

@router.get("/locations/{location_reference}")
def read_location_details(
    location_reference: str,
    db: Session = Depends(get_db),
) -> LocationDetailedResponse:
    return get_detailed_location(db, location_reference)
