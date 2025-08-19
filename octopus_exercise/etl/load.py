from typing import List

from ..db.session import engine, SessionLocal
from sqlalchemy.orm import Session

from ..db.models import LocationTableModel, OperatorTableModel, EvsesTableModel, ConnectorTableModel, Base
from .transform import LocationETLModel, EvsesETLModel, OperatorETLModel, ConnectorETLModel, CoordinatesETLModel

def load_locations_into_db(locations: List[LocationETLModel]):
    locationTableModels: List[LocationTableModel] = build_table_models(locations)
    persist(engine, locationTableModels)

def build_connector_table_models(connectors: List[ConnectorETLModel]) -> List[ConnectorTableModel]:
    connector_table_models: List[ConnectorTableModel] = []
    for connector in connectors:
        connector_table_model: ConnectorTableModel = ConnectorTableModel(
            power_type=connector.power_type,
            max_amperage=connector.max_amperage,
            max_voltage=connector.max_voltage,
            max_electric_power=connector.max_electric_power,
            standard=connector.standard,
        )
        connector_table_models.append(connector_table_model)
        
    return connector_table_models

def build_evses_table_models(evses: List[EvsesETLModel]) -> List[EvsesTableModel]:
    evses_table_models: List[EvsesTableModel] = []
    for evse in evses:
        evse_table_model: EvsesTableModel = EvsesTableModel(
            physical_reference= evse.physical_reference,
            status=evse.status,
            connectors=build_connector_table_models(evse.connectors)
        )
        evses_table_models.append(evse_table_model)
    return evses_table_models

def build_operator_table_models(operator: OperatorETLModel | None) -> OperatorTableModel | None:
    if operator is None:
        return None
    return OperatorTableModel(name=operator.name)

def build_table_models(locations: List[LocationETLModel]) -> List[LocationTableModel]:
    location_table_models: List[LocationTableModel] = []
    for location in locations:
        location_table_model = LocationTableModel(
            address=location.address,
            latitude=location.coordinates.latitude,
            longitude=location.coordinates.longitude,
            reference=location.id,
            name=location.name,
            postal_code=location.postal_code,
            country=location.country,
            operator=build_operator_table_models(location.operator),
            evses=build_evses_table_models(location.evses),

        )
        location_table_models.append(location_table_model)
    return location_table_models

def persist(engine, locations: List[LocationTableModel]):
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    session.add_all(locations)
    session.commit()

##################################################################################################
# Didn't get around to finishing this. It is for loading the SQLAlchemy table models into memory #
# and converting them into ETL models so I can merge similar locations based on their location   #
# data                                                                                           #
##################################################################################################
def load_locations_into_memory(session: Session) -> List[LocationETLModel]:
    locations_table_models: List[LocationTableModel] = session.query(LocationTableModel).all()
    existing_etl_models: List[LocationETLModel] = []

    for existing_location in locations_table_models:
        location: LocationETLModel = LocationETLModel(
            address=existing_location.address,
            postal_code=existing_location.postal_code,
            id=existing_location.id,
            name=existing_location.name,
            country=existing_location.country,
            evses=existing_location.evses,
            operator=OperatorETLModel(name=existing_location.operator.name),
            coordinates=CoordinatesETLModel(
                latitude=existing_location.latitude,
                longitude=existing_location.longitude,
            )
        )
        locations_table_models.append(location)
    return existing_etl_models

def build_evses_etl_models(evses: List[EvsesTableModel]) -> List[EvsesETLModel]:
    evses_table_models: List[EvsesETLModel] = []
    for evse in evses:
        evse_etl_model: EvsesETLModel = EvsesETLModel(
            physical_reference=str(evse.physical_reference),
            status=str(evse.status),
            connectors=[]
        )
        evses_table_models.append(evse_etl_model)
    return evses_table_models

def build_connector_etl_models(connectors: List[ConnectorETLModel]) -> List[ConnectorTableModel]:
    return []

