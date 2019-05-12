from sqlalchemy.orm import Session

from DAOs.AlertsDAO import AlertsDAO
from DAOs.DBConnector import DBConnector
from DAOs.FirefightersDAO import FirefightersDAO
from DAOs.SessionProvider import SessionProvider
from DataBaseModel import Alert, Person
from Exceptions.Exceptions import ObjectAlreadyExistsInCollectionException, ObjectNotFoundInCollectionException, \
    ObjectNotFoundInDBException


class FirefightersAlertsController:
    alerts_dao: AlertsDAO = None
    firefighters_dao: FirefightersDAO = None
    session: Session = None

    def __init__(self):
        sp = SessionProvider()
        self.session = sp.get_session()
        connector = DBConnector(self.session)
        self.alerts_dao = AlertsDAO(connector)
        self.firefighters_dao = FirefightersDAO(connector)

    def assign_firefighter_to_alert(self, firefighter_id: int, alert_id: int) -> None:
        try:
            if isinstance(firefighter_id, int) and isinstance(alert_id, int):
                firefighter = self.firefighters_dao.get(firefighter_id)

                if firefighter.is_active is False:
                    raise ObjectNotFoundInDBException

                alert = self.alerts_dao.get(alert_id)

                if not any(alert.id == a.id for a in firefighter.alerts):
                    firefighter.alerts.append(alert)
                    self.session.commit()
                else:
                    raise ObjectAlreadyExistsInCollectionException
            else:
                raise ValueError
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def discharge_firefighter_from_alert(self, firefighter_id: int, alert_id: int) -> None:
        try:
            if isinstance(firefighter_id, int) and isinstance(alert_id, int):
                firefighter = self.firefighters_dao.get(firefighter_id)
                alert = self.alerts_dao.get(alert_id)

                if any(alert.id == a.id for a in firefighter.alerts):
                    firefighter.alerts.remove(alert)
                    self.session.commit()
                else:
                    raise ObjectNotFoundInCollectionException
            else:
                raise ValueError
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def get_firefighters_assigned_to_alert_info(self, alert_id: int) -> str:
        try:
            if isinstance(alert_id, int):
                alert = self.alerts_dao.get(alert_id)
                return "[{0}]".format(str.join(",", [f.to_list_json() for f in alert.persons]))
            else:
                raise ValueError
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def get_firefighter_alerts_info(self, firefighter_id: int) -> str:
        try:
            if isinstance(firefighter_id, int):
                firefighter = self.firefighters_dao.get(firefighter_id)
                return "[{0}]".format(str.join(",", [a.to_list_json() for a in firefighter.alerts]))
            else:
                raise ValueError
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def get_alert_info(self, firefighter_id: int, alert_id: int) -> str:
        return self.get_alert_connected_to_firefighter(int(alert_id), int(firefighter_id)).to_full_json()

    def get_firefighter_info(self, alert_id: int, firefighter_id: int) -> str:
        return self.get_firefighter_connected_to_alert(int(alert_id), int(firefighter_id)).to_full_json()

    def get_alert_connected_to_firefighter(self, alert_id: int, firefighter_id: int) -> Alert:
        try:
            if isinstance(firefighter_id, int) and isinstance(alert_id, int):
                firefighter = self.firefighters_dao.get(firefighter_id)
                if firefighter is None:
                    raise ObjectNotFoundInDBException

                alert = next((a for a in firefighter.alerts if a.id == alert_id), None)
                if alert is None:
                    raise ObjectNotFoundInDBException

                return alert
            else:
                raise ValueError
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def get_firefighter_connected_to_alert(self, alert_id: int, firefighter_id: int) -> Person:
        try:
            if isinstance(firefighter_id, int) and isinstance(alert_id, int):
                alert = self.alerts_dao.get(alert_id)
                if alert is None:
                    raise ObjectNotFoundInDBException

                firefighter = next((p for p in alert.persons if p.id == firefighter_id), None)
                if firefighter is None:
                    raise ObjectNotFoundInDBException

                return firefighter
            else:
                raise ValueError
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()
