from DAOs.DBConnector import DBConnector
from DataBaseModel import Firefighter


class FirefightersDAO:
    connector = DBConnector()

    def query_all(self):
        return self.connector.query_from_db(Firefighter).all()

    def get(self, firefighter_id):
        return self.connector.get_by_id(Firefighter, firefighter_id)

    def add(self, firefighter):
        self.connector.add_to_db(firefighter)

    def query_all_in_list_json(self):
        all_firefighters = self.query_all()
        return "[" + str.join(",", [a.to_list_json() for a in all_firefighters]) + "]"

    def get_full_in_json(self, firefighter_id):
        firefighter = self.get(firefighter_id)
        if firefighter is not None:
            return firefighter.to_full_json()
        else:
            return None
