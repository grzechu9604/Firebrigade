import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


alerts_vehicles = Table('alerts_vehicles', Base.metadata,
                        Column('alert_id', Integer, ForeignKey('Alerts.id')),
                        Column('vehicle_id', Integer, ForeignKey('Vehicles.id')))

alerts_people = Table('alerts_people', Base.metadata,
                      Column('alert_id', Integer, ForeignKey('Alerts.id')),
                      Column('person_id', Integer, ForeignKey('People.id')))


class Person(Base):
    __tablename__ = 'People'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    birth_date = Column(Date(), nullable=False)
    alerts = relationship("Alert", secondary=alerts_people, back_populates="persons")


class HonoraryMember(Base):
    __tablename__ = 'HonoraryMembers'
    is_active = Column(Boolean, nullable=False)
    person_id = Column(Integer, ForeignKey('People.id'), primary_key=True)
    person = relationship(Person)


class Firefighter(Base):
    __tablename__ = 'Firefighters'
    is_active = Column(Boolean, nullable=False)
    person_id = Column(Integer, ForeignKey('People.id'), primary_key=True)
    person = relationship(Person)


class Alert(Base):
    __tablename__ = 'Alerts'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    reason = Column(String(500), nullable=False)
    persons = relationship("Person", secondary=alerts_people, back_populates="alerts_persons")
    vehicles = relationship("Vehicle", secondary=alerts_vehicles, back_populates="alerts_vehicles")


class Vehicle(Base):
    __tablename__ = 'Vehicles'
    id = Column(Integer, primary_key=True)
    type = Column(String(500), nullable=False)
    name = Column(String(500), nullable=False)
    description = Column(String(500), nullable=False)
    seats_amount = Column(Integer, nullable=False)
    alerts = relationship("Alert", secondary=alerts_vehicles, back_populates="alerts")


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///fire_brigade.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
