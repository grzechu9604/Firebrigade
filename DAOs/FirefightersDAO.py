from typing import List, Optional

from sqlalchemy.orm.exc import NoResultFound

from DAOs.DBConnector import DBConnector
from DAOs.PersonsDAO import PersonsDAO
from DataBaseModel import Firefighter


class FirefightersDAO:
    connector: DBConnector = None

    def __init__(self, connector: DBConnector):
        self.connector = connector

    def query_all_active(self) -> List[Firefighter]:
        return self.connector.query_from_db(Firefighter).filter(Firefighter.is_active == 1).all()

    def query_all(self) -> List[Firefighter]:
        return self.connector.query_from_db(Firefighter).all()

    def get(self, firefighter_id: int) -> Firefighter:
        return self.connector.get_by_id(Firefighter, firefighter_id)

    def add(self, firefighter: Firefighter) -> None:
        self.connector.add_to_db(firefighter)

    def get_same(self, firefighter: Firefighter) -> Optional[Firefighter]:
        try:
            persons_dao = PersonsDAO(self.connector)
            same_person = persons_dao.get_same(firefighter.person)

            if same_person is not None:
                return self.get(same_person.id)
        except NoResultFound:
            return None

    def query_page_active(self, page_no: int = 1, records_per_page: int = 10) -> List[Firefighter]:
        return self.connector.query_from_db(Firefighter).filter(Firefighter.is_active == 1).\
                limit(records_per_page).offset((page_no - 1) * records_per_page).all()
