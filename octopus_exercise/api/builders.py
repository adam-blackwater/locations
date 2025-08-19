from octopus_exercise.api.models import LocationsResponse, LocationDetailedResponse, Location, Coordinates, EVSE, Connector
from typing import List, Union

def build_locations_response(locations) -> LocationsResponse:
    location_responses: List[Location] = []
    for location in locations:
        location_response: Location = Location(
            coordinates=Coordinates(
                lat=location.latitude,
                lon=location.longitude,
            ),
            operator_reference=build_operator_response(location.operator),
            country_reference=location.country,
            postal_code=location.postal_code,
            number_of_evses=len(location.evses)
            
        )
        location_responses.append(location_response)
    return LocationsResponse(locations=location_responses)

def build_detailed_location_response(location) -> LocationDetailedResponse:
    location_detailed_response: LocationDetailedResponse = LocationDetailedResponse(
        coordinates=Coordinates(
            lat=location.latitude,
            lon=location.longitude,
        ),
        operator_reference=build_operator_response(location.operator),
        country_reference=location.country,
        postal_code=location.postal_code,
        evses=build_evses_response(location.evses)
    )
    return location_detailed_response

def build_evses_response(evses) -> List[EVSE]:
    evses_response: List[EVSE] = []
    for evse in evses:
        evse_response: EVSE = EVSE(
            physical_identifier=evse.physical_reference,
            status=evse.status,
            connectors=build_connectors_response(evse.connectors)
        )
        evses_response.append(evse_response)
    return evses_response

def build_operator_response(operator) -> int | str | None:
    if operator is None:
        return None
    return operator.name

def build_connectors_response(connectors) -> List[Connector]:
    connectors_response: List[Connector] = []
    for connector in connectors:
        connector_response: Connector = Connector(
            power=connector.max_electric_power,
            standard=connector.standard,
        )
        connectors_response.append(connector_response)
    return connectors_response
