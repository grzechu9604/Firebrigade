from datetime import datetime
from sqlalchemy.orm import Session

from DAOs.DBConnector import DBConnector
from DAOs.FirefightersDAO import FirefightersDAO
from DAOs.SessionProvider import SessionProvider
from DataBaseModel import Firefighter
from Exceptions.Exceptions import ObjectNotFoundInDBException, ObjectExistsInDBException


class FirefightersController:
    dao: FirefightersDAO = None
    session: Session = None

    def __init__(self):
        sp = SessionProvider()
        self.session = sp.get_session()
        connector = DBConnector(self.session)
        self.dao = FirefightersDAO(connector)

    def get_firefighter(self, firefighter_id: int) -> Firefighter:
        try:
            if isinstance(firefighter_id, int):
                return self.dao.get(firefighter_id)
            else:
                raise ValueError
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def get_active_firefighter(self, firefighter_id: int) -> Firefighter:
        try:
            f = self.get_firefighter(firefighter_id)
            if f is not None and f.is_active is True:
                return f
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def get_active_firefighter_info_in_json(self, firefighter_id: int) -> str:
        try:
            firefighter = self.get_active_firefighter(firefighter_id)
            if firefighter is None:
                raise ObjectNotFoundInDBException
            else:
                return firefighter.to_full_json()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def get_firefighter_info_in_json(self, firefighter_id: int) -> str:
        try:
            firefighter = self.get_firefighter(firefighter_id)
            if firefighter is None:
                raise ObjectNotFoundInDBException
            else:
                return firefighter.to_full_json()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def get_active_firefighters_info_in_json(self) -> str:
        try:
            return str.format("[{0}]", str.join(",", [f.to_list_json() for f in self.dao.query_all_active()]))
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def deactivate_firefighter(self, firefighter_id: int) -> None:
        try:
            firefighter = self.get_firefighter(firefighter_id)
            if firefighter is None or firefighter.is_active is False:
                raise ObjectNotFoundInDBException
            else:
                firefighter.is_active = False
                self.dao.add(firefighter)
                self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def create_firefighter(self, name: str, last_name: str, birth_date_str: str) -> None:
        try:
            if name is None or last_name is None or len(name) == 0 or len(last_name) == 0:
                raise ValueError

            birth_date = None
            if birth_date_str is not None and len(birth_date_str) > 0:
                birth_date = self.get_time_from_string_timestamp(birth_date_str)

            firefighter = Firefighter(name=name, last_name=last_name, birth_date=birth_date, is_active=True)
            existing_firefighter = self.dao.get_same(firefighter)
            if existing_firefighter is not None:
                raise ObjectExistsInDBException(existing_firefighter.id)

            self.dao.add(firefighter)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def update_firefighter_partially(self, firefighter_id, name, last_name, birth_date_str) -> None:
        try:
            firefighter = self.dao.get(firefighter_id)
            if firefighter is None or firefighter.is_active is False:
                raise ObjectNotFoundInDBException

            if name is not None and len(name) > 0:
                firefighter.name = name

            if last_name is not None and len(last_name) > 0:
                firefighter.last_name = last_name

            if birth_date_str is not None and len(birth_date_str) > 0:
                firefighter.birth_date = self.get_time_from_string_timestamp(birth_date_str)

            self.dao.add(firefighter)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def update_firefighter_fully(self, firefighter_id, name, last_name, birth_date_str) -> None:
        try:
            firefighter = self.dao.get(firefighter_id)
            if firefighter is None or firefighter.is_active is False:
                raise ObjectNotFoundInDBException

            if name is None or len(name) == 0 or last_name is None or len(last_name) == 0:
                raise ValueError

            if birth_date_str is not None and len(birth_date_str) > 0:
                firefighter.birth_date = self.get_time_from_string_timestamp(birth_date_str)
            else:
                firefighter.birth_date = None

            firefighter.last_name = last_name
            firefighter.name = name

            self.dao.add(firefighter)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    @staticmethod
    def get_time_from_string_timestamp(timestamp_string: str) -> datetime:
        return datetime.strptime(timestamp_string, '%Y-%m-%d')
