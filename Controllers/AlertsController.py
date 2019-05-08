from datetime import datetime

from DAOs.AlertsDAO import AlertsDAO
from DataBaseModel import Alert
from Exceptions.Exceptions import ObjectNotFoundInDBException


class AlertsController:
    dao = AlertsDAO()

    def get_alert(self, alert_id: int) -> Alert:
        if isinstance(alert_id, int):
            return self.dao.get(alert_id)
        else:
            raise ValueError

    def query_all_in_list_json(self) -> str:
        all_alerts = self.dao.query_all()
        return "[" + str.join(",", [a.to_list_json() for a in all_alerts]) + "]"

    def get_full_in_json(self, alert_id: int) -> str:
        alert = self.dao.get(alert_id)
        if alert is not None:
            return alert.to_full_json()
        else:
            raise ObjectNotFoundInDBException

    def create_alert(self, reason: str, timestamp: str) -> None:
        if reason is None or timestamp is None or len(reason) == 0:
            raise ValueError

        alert = Alert(reason=reason, timestamp=self.get_time_from_string_timestamp(timestamp))
        self.dao.add(alert)

    def update_alert_partially(self, alert_id: int, reason: str, timestamp: str) -> None:
        alert: Alert = self.dao.get(alert_id)
        if alert is None:
            raise ObjectNotFoundInDBException

        if reason is not None and len(reason) > 0:
            alert.reason = reason

        if timestamp is not None:
            alert.timestamp = self.get_time_from_string_timestamp(timestamp)

        self.dao.add(alert)

    def update_alert_fully(self, alert_id: int, reason: str, timestamp:str):
        alert: Alert = self.dao.get(alert_id)
        if alert is None:
            raise ObjectNotFoundInDBException

        if reason is None or len(reason) > 0 or timestamp is None:
            raise ValueError

        alert.reason = reason
        alert.timestamp = self.get_time_from_string_timestamp(timestamp)

        self.dao.add(alert)

    def delete_alert(self, alert_id: int) -> None:
        alert: Alert = self.dao.get(alert_id)
        if alert is None:
            raise ObjectNotFoundInDBException

        self.dao.delete_alert(alert)

    @staticmethod
    def get_time_from_string_timestamp(timestamp_string: str):
        return datetime.strptime(timestamp_string, '%Y-%m-%dT%H:%M:%S')
