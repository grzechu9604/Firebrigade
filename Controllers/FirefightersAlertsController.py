from Controllers.FirefightersController import FirefightersController
from DAOs.DBConnector import DBConnector
from DAOs.AlertsDAO import AlertsDAO
from Exceptions.Exceptions import ObjectAlreadyExistsInCollectionException, ObjectNotFoundInCollectionException


class FirefightersAlertsController:
    alerts_dao = AlertsDAO()
    firefighters_controller = FirefightersController()
    db_connector = DBConnector()

    def assign_firefighter_to_alert(self, firefighter_id: int, alert_id: int) -> None:
        if isinstance(firefighter_id, int) and isinstance(alert_id, int):
            firefighter = self.firefighters_controller.get_active_firefighter(firefighter_id)
            alert = self.alerts_dao.get(alert_id)

            if not any(alert.id == a.id for a in firefighter.alerts):
                firefighter.alerts.append(alert)
                self.db_connector.commit_session()
            else:
                self.db_connector.rollback_session()
                raise ObjectAlreadyExistsInCollectionException
        else:
            self.db_connector.rollback_session()
            raise ValueError

    def discharge_firefighter_from_alert(self, firefighter_id: int, alert_id: int) -> None:
        if isinstance(firefighter_id, int) and isinstance(alert_id, int):
            firefighter = self.firefighters_controller.get_firefighter(firefighter_id)
            alert = self.alerts_dao.get(alert_id)

            if any(alert.id == a.id for a in firefighter.alerts):
                firefighter.alerts.remove(alert)
                self.db_connector.commit_session()
            else:
                self.db_connector.rollback_session()
                raise ObjectNotFoundInCollectionException
        else:
            self.db_connector.rollback_session()
            raise ValueError

    def get_firefighters_assigned_to_alert_info(self, alert_id: int) -> str:
        if isinstance(alert_id, int):
            alert = self.alerts_dao.get(alert_id)
            return "[{0}]".format(str.join(",", [f.to_list_json() for f in alert.persons]))
        else:
            self.db_connector.rollback_session()
            raise ValueError

    def get_firefighter_alerts_info(self, firefighter_id: int) -> str:
        if isinstance(firefighter_id, int):
            firefighter = self.firefighters_controller.get_firefighter(firefighter_id)
            return "[{0}]".format(str.join(",", [a.to_list_json() for a in firefighter.alerts]))
        else:
            self.db_connector.rollback_session()
            raise ValueError
