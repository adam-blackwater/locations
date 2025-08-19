import math
from typing import Any, Dict, List, Optional
from octopus_exercise.utils.geolocation import haversine
from enum import Enum

from pydantic import BaseModel, ConfigDict, model_validator


class PowerTypeEnum(str, Enum):
    AC_1_PHASE = 'AC_1_PHASE'
    AC_3_PHASE = 'AC_3_PHASE'
    DC = 'DC'

class ConnectorETLModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, strict=False)

    power_type: Optional[str] = None
    max_amperage: Optional[int] = None
    max_voltage: Optional[int] = None
    max_electric_power: Optional[int] = None
    standard: Optional[str] = None

    @staticmethod
    def three_phase_converstion(amps: int, volts: int) -> int:
        return round(math.sqrt(3) * volts * amps / 1000) * 1000

    @staticmethod
    def single_phase_conversion(amps: int, volts: int) -> int:
        return round(amps * volts / 1000) * 1000

    @model_validator(mode="after")
    def compute_max_electric_power(cls, model):
        if model.max_electric_power is not None:
            return model

        max_amperage: int = int(model.max_amperage)
        max_voltage: int = int(model.max_voltage)
        power_type: str = str(model.power_type)

        if PowerTypeEnum.AC_3_PHASE.name == power_type:
            model.max_electric_power = cls.three_phase_converstion(max_amperage, max_voltage)
            return model
        model.max_electric_power = cls.single_phase_conversion(max_amperage, max_voltage)
        return model


class EvsesETLModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, strict=False)

    physical_reference: str
    status: str
    connectors: List[ConnectorETLModel]


class OperatorETLModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, strict=False)

    name: str = ""


class CoordinatesETLModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, strict=False)

    latitude: str
    longitude: str


class LocationETLModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, strict=False)

    address: str
    coordinates: CoordinatesETLModel
    postal_code: str
    id: str
    name: str
    country: str
    evses: List[EvsesETLModel]
    operator: Optional[OperatorETLModel] = None

def compare_locations(new_location: LocationETLModel, existing_locations: List[LocationETLModel]) -> Optional[LocationETLModel]:
    for existing_location in existing_locations:
        proximity = haversine(
            new_location.coordinates.latitude,
            new_location.coordinates.longitude,
            existing_location.coordinates.latitude,
            existing_location.coordinates.longitude,
        )
        if proximity <= 10:
            return existing_location
        return None
            
def transform(data: Dict[str, Any], existing: Optional[List[LocationETLModel]] = None) -> List[LocationETLModel]:
    ###########################################################################################
    # This function has incomplte code in it. I didn't have time to finish this part but I    #
    # left it in so you could see what I was thinking at the time                             #
    #                                                                                         #
    # The existing function parameter is Optional and defaults to None just because I didn't  #
    # have time to complete this functionality                                                #
    ###########################################################################################
     
    # combined_locations = existing.copy()

    # for location in data:
    #     transformed_new_location = LocationETLModel.model_validate(location)
    #     combined_locations.append(transformed_new_location)
    #     matched_existing_location = compare_locations(transformed_new_location, existing)

    #     if matched_existing_location:
    #         merge_locations(transformed_new_location, matched_existing_location)
    #     else:
    #         combined_locations.append(transformed_new_location)

    # return combined_locations
    
    etl_models: List[LocationETLModel] = []

    for item in data:
        etl_models.append(LocationETLModel.model_validate(item))

    return etl_models

##################################################################################################
# Didn't get around to finishing this. It is for merging two locations                           #
##################################################################################################
def merge_locations(new_location: LocationETLModel, existing_location: LocationETLModel):
    # Updating the existing location here so that later on the load step in the ETL
    # will commit the new location data as the existing_location object is an SQLAlchemy
    # object that is tracked by the sqlalchemy engine
    existing_location.operator = new_location.operator

