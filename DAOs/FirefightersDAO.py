from typing import List

from DAOs.DBConnector import DBConnector
from DataBaseModel import Firefighter


class FirefightersDAO:
    connector = DBConnector()

    def query_all_active(self) -> List[Firefighter]:
        return self.connector.query_from_db(Firefighter).filter(Firefighter.is_active == 1).all()

    def query_all(self) -> List[Firefighter]:
        return self.connector.query_from_db(Firefighter).all()

    def get(self, firefighter_id: int) -> Firefighter:
        return self.connector.get_by_id(Firefighter, firefighter_id)

    def add(self, firefighter: Firefighter):
        try:
            self.connector.add_to_db(firefighter)
            self.connector.session.commit()
        except Exception as e:
            self.connector.session.rollback()
            raise e
