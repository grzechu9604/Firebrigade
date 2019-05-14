from typing import Optional

from datetime import date
from sqlalchemy.orm.exc import NoResultFound

from DAOs.DBConnector import DBConnector
from DataBaseModel import Person


class PersonsDAO:
    connector: DBConnector = None

    def __init__(self, connector: DBConnector):
        self.connector = connector

    def _get_same(self, birth_date: date, name: str, last_name: str) -> Optional[Person]:
        try:
            return self.connector.query_from_db(Person)\
                    .filter(Person.birth_date == birth_date,
                            Person.name == name,
                            Person.last_name == last_name).first()
        except NoResultFound:
            return None

    def get_same(self, person: Person) -> Optional[Person]:
        return self._get_same(person.birth_date, person.name, person.last_name)

    def get(self, person_id: int) -> Optional[Person]:
        return self.connector.get_by_id(Person, person_id)
