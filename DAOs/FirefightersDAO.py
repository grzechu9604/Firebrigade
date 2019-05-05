from typing import Optional, Any

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
        firefighter: Firefighter = self.get(firefighter_id)
        if firefighter is not None:
            return firefighter.to_full_json()
        else:
            return None

    def deactivate_firefighter(self, firefighter_id):
        firefighter: Firefighter = self.get(firefighter_id)
        if firefighter is None or firefighter.is_active is False:
            return False
        else:
            firefighter.is_active = False
            self.connector.session.add(firefighter)
            return True

    def create_firefighter(self, name, last_name, birth_date):
        if name is None or last_name is None or len(name) == 0 or len(last_name) == 0:
            return False

        try:
            firefighter = Firefighter(name=name, last_name=last_name, birth_date=birth_date, is_active=True)
            self.add(firefighter)
            return True
        except:
            return False

    def update_firefighter_partially(self, firefighter_id, name, last_name, birth_date):
        firefighter: Firefighter = self.get(firefighter_id)
        if firefighter is None or firefighter.is_active is False:
            return False

        if name is not None and len(name) > 0:
            firefighter.name = name

        if last_name is not None and len(last_name) > 0:
            firefighter.last_name = last_name

        if birth_date is not None:
            firefighter.birth_date = birth_date

        DBConnector.session.add(firefighter)
        return True

    def update_firefighter_fully(self, firefighter_id, name, last_name, birth_date):
        firefighter: Firefighter = self.get(firefighter_id)
        if firefighter is None or firefighter.is_active is False:
            return False

        firefighter.name = name
        firefighter.last_name = last_name
        firefighter.birth_date = birth_date

        DBConnector.session.add(firefighter)
        return True
