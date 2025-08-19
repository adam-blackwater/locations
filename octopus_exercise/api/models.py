from typing import List, Union
from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    lat: float = Field(..., description="Latitude of the location")
    lon: float = Field(..., description="Longitude of the location")


class Location(BaseModel):
    coordinates: Coordinates
    operator_reference: Union[int, str] | None = Field(..., description="Operator reference ID or code")
    country_reference: str = Field(..., description="Country code")
    postal_code: str = Field(..., description="Postal code")
    number_of_evses: int = Field(..., description="Number of EVSEs at the location")


class LocationsResponse(BaseModel):
    locations: List[Location]


class Connector(BaseModel):
    power: int = Field(..., description="Power of the connector in kW")
    standard: str = Field(..., description="Connector standard/type")


class EVSE(BaseModel):
    physical_identifier: str = Field(..., description="Physical identifier of the EVSE")
    status: str = Field(..., description="Current status of the EVSE")
    connectors: List[Connector] = Field(..., description="List of connectors for this EVSE")


class LocationDetailedResponse(BaseModel):
    coordinates: Coordinates
    operator_reference: Union[int, str] | None = Field(..., description="Operator reference ID or code")
    country_reference: str = Field(..., description="Country code")
    postal_code: str = Field(..., description="Postal code")
    evses: List[EVSE] = Field(..., description="List of EVSEs at the location")
