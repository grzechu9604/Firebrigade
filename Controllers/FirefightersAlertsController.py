from DAOs.FirefightersDAO import FirefightersDAO
from DAOs.AlertsDAO import AlertsDAO
from Exceptions.Exceptions import ObjectAlreadyExistsInCollectionException, ObjectNotFoundInCollectionException


class FirefightersAlertsController:
    firefighters_dao = FirefightersDAO()
    alerts_dao = AlertsDAO()

    def assign_firefighter_to_alert(self, firefighter_id: int, alert_id: int):
        if isinstance(firefighter_id, int) and isinstance(alert_id, int):
            firefighter = self.firefighters_dao.get(firefighter_id)
            alert = self.alerts_dao.get(alert_id)

            if not any(alert.id == a.id for a in firefighter.alerts):
                firefighter.alerts.append(alert)
                self.firefighters_dao.connector.session.commit()
            else:
                self.firefighters_dao.connector.session.rollback()
                raise ObjectAlreadyExistsInCollectionException
        else:
            self.firefighters_dao.connector.session.rollback()
            raise ValueError

    def discharge_firefighter_from_alert(self, firefighter_id: int, alert_id: int):
        if isinstance(firefighter_id, int) and isinstance(alert_id, int):
            firefighter = self.firefighters_dao.get(firefighter_id)
            alert = self.alerts_dao.get(alert_id)

            if any(alert.id == a.id for a in firefighter.alerts):
                firefighter.alerts.remove(alert)
                self.firefighters_dao.connector.session.commit()
            else:
                self.firefighters_dao.connector.session.rollback()
                raise ObjectNotFoundInCollectionException
        else:
            self.firefighters_dao.connector.session.rollback()
            raise ValueError

    def get_firefighters_assigned_to_alert_info(self, alert_id: int) -> str:
        if isinstance(alert_id, int):
            alert = self.alerts_dao.get(alert_id)
            return "[{0}]".format(str.join(",", [f.to_list_json() for f in alert.persons]))
        else:
            self.firefighters_dao.connector.session.rollback()
            raise ValueError

    def get_firefighter_alerts_info(self, firefighter_id: int) -> str:
        if isinstance(firefighter_id, int):
            firefighter = self.firefighters_dao.get(firefighter_id)
            return "[{0}]".format(str.join(",", [a.to_list_json() for a in firefighter.alerts]))
        else:
            self.firefighters_dao.connector.session.rollback()
            raise ValueError
