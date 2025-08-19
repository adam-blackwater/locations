import sqlalchemy as sa
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class ConnectorTableModel(Base):
    __tablename__ = "connectors"
    id = sa.Column('id', sa.Integer, primary_key=True)
    power_type = Column(String)
    max_amperage = Column(String)
    max_voltage = Column(String)
    max_electric_power = Column(String)
    standard = Column(String)
    evse_id = Column(Integer, ForeignKey("evses.id"))
    evse = relationship("EvsesTableModel", back_populates="connectors")


class EvsesTableModel(Base):
    __tablename__ = "evses"
    id = sa.Column('id', sa.Integer, primary_key=True)
    physical_reference= Column(String)
    status = Column(String)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    location = relationship("LocationTableModel", back_populates="evses")
    connectors = relationship("ConnectorTableModel", back_populates="evse", cascade="all, delete-orphan")


class OperatorTableModel(Base):
    __tablename__ = "operators"
    id = sa.Column('id', sa.Integer, primary_key=True)
    name = Column(String)
    location = relationship("LocationTableModel", back_populates="operator", cascade="all, delete-orphan", single_parent=True)


class LocationTableModel(Base):
    __tablename__ = "locations"
    id = sa.Column('id', sa.Integer, primary_key=True)
    address = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    reference = Column(String)
    name = Column(String)
    postal_code = Column(String)
    country = Column(String)
    operator_id = Column(Integer, ForeignKey("operators.id"))
    operator = relationship("OperatorTableModel", back_populates="location")
    evses = relationship("EvsesTableModel", back_populates="location", cascade="all, delete-orphan")
