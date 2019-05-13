from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from Helpers.SerializationHelper import SerializationHelper

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
    birth_date = Column(Date(), nullable=True)
    alerts = relationship("Alert", secondary=alerts_people, back_populates="persons")

    def to_list_json(self):
        sh = SerializationHelper()
        sh.name = self.name
        sh.last_name = self.last_name
        sh.id = self.id
        return sh.to_json()

    def to_full_json(self):
        sh = SerializationHelper()
        sh.name = self.name
        sh.last_name = self.last_name
        sh.id = self.id
        sh.birth_date = self.birth_date
        return sh.to_json()


class HonoraryMember(Person):
    __tablename__ = 'HonoraryMembers'

    is_active = Column(Boolean, nullable=False)
    person_id = Column(Integer, ForeignKey('People.id'), primary_key=True)
    person = relationship(Person)

    def to_list_json(self):
        sh = SerializationHelper()
        sh.name = self.name
        sh.last_name = self.last_name
        sh.id = self.id
        sh.link = "~/honoraryMembers/" + str(self.id)
        return sh.to_json()

    def to_full_json(self):
        sh = SerializationHelper()
        sh.name = self.name
        sh.last_name = self.last_name
        sh.id = self.id
        sh.birth_date = self.birth_date
        return sh.to_json()


class Firefighter(Person):
    __tablename__ = 'Firefighters'

    is_active = Column(Boolean, nullable=False)
    person_id = Column(Integer, ForeignKey('People.id'), primary_key=True)
    person = relationship(Person)

    def to_list_json(self):
        sh = SerializationHelper()
        sh.name = self.name
        sh.last_name = self.last_name
        sh.id = self.id
        sh.link = "~/firefighters/" + str(self.id)
        return sh.to_json()

    def to_full_json(self):
        sh = SerializationHelper()
        sh.name = self.name
        sh.last_name = self.last_name
        sh.id = self.id
        sh.birth_date = self.birth_date
        return sh.to_json()


class Alert(Base):
    __tablename__ = 'Alerts'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    reason = Column(String(500), nullable=False)
    persons = relationship("Person", secondary=alerts_people, back_populates="alerts")
    vehicles = relationship("Vehicle", secondary=alerts_vehicles, back_populates="alerts")

    def to_list_json(self):
        sh = SerializationHelper()
        sh.timestamp = self.timestamp
        sh.reason = self.reason
        sh.id = self.id
        sh.link = "~/alerts/" + str(self.id)
        return sh.to_json()

    def to_full_json(self):
        sh = SerializationHelper()
        sh.timestamp = self.timestamp
        sh.reason = self.reason
        sh.id = self.id
        return sh.to_json()


class Vehicle(Base):
    __tablename__ = 'Vehicles'

    id = Column(Integer, primary_key=True)
    type = Column(String(500), nullable=False)
    name = Column(String(500), nullable=False)
    description = Column(String(500), nullable=False)
    seats_amount = Column(Integer, nullable=False)
    alerts = relationship("Alert", secondary=alerts_vehicles, back_populates="vehicles")

    def to_list_json(self):
        sh = SerializationHelper()
        sh.type = self.type
        sh.name = self.name
        sh.id = self.id
        sh.link = "~/vehicles/" + str(self.id)
        return sh.to_json()

    def to_full_json(self):
        sh = SerializationHelper()
        sh.type = self.type
        sh.name = self.name
        sh.id = self.id
        sh.description = self.description
        sh.seats_amount = self.seats_amount
        return sh.to_json()


engine = create_engine('sqlite:///fire_brigade.db')
Base.metadata.create_all(engine)
