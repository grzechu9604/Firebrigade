import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from DataBaseModel import Base, Firefighter, HonoraryMember, Vehicle, Alert

engine = create_engine('sqlite:///fire_brigade.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

new_firefighter = Firefighter(name='Janina', last_name='Nowak', is_active=True)
new_firefighter2 = Firefighter(name='Jan', last_name='Nowak', is_active=True)
new_member = HonoraryMember(name='Janko', last_name='Nowak', is_active=False)
new_member2 = HonoraryMember(name='Janinka', last_name='Nowak', is_active=True)
new_vehicle = Vehicle(type='GCBA', name='Ciężki', description='Gaśniczy ciężki bojowy z autopompą', seats_amount=6)
new_alert = Alert(timestamp=datetime.datetime.now(), reason='Pożar śmietnika')

new_alert.vehicles = [new_vehicle]
new_alert.persons = [new_firefighter, new_firefighter2]

session.add(new_firefighter)
session.add(new_firefighter2)
session.add(new_member)
session.add(new_member2)
session.add(new_vehicle)
session.add(new_alert)
session.commit()
