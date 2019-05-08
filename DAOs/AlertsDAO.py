from datetime import datetime

from DAOs.DBConnector import DBConnector
from DataBaseModel import Alert


class AlertsDAO:
    connector = DBConnector()

    def query_all(self):
        return self.connector.query_from_db(Alert).all()

    def get(self, alert_id: int) -> Alert:
        return self.connector.get_by_id(Alert, alert_id)

    def add(self, alert: Alert):
        self.connector.add_to_db(alert)

    def query_all_in_list_json(self):
        all_alerts = self.query_all()
        return "[" + str.join(",", [a.to_list_json() for a in all_alerts]) + "]"

    def get_full_in_json(self, alert_id):
        alert: Alert = self.get(alert_id)
        if alert is not None:
            return alert.to_full_json()
        else:
            return None

    def delete_alert(self, alert_id):
        alert: Alert = self.get(alert_id)
        if alert is None:
            return False
        else:
            self.connector.session.delete(alert)
            self.connector.session.commit()
            return True

    def create_alert(self, reason, timestamp):
        if reason is None or timestamp is None or len(reason) == 0:
            return False

        try:
            alert = Alert(reason=reason, timestamp=self.get_time_from_string_timestamp(timestamp))
            self.add(alert)
            self.connector.session.commit()
            return True
        except:
            return False

    def update_alert_partially(self, alert_id, reason, timestamp):
        alert: Alert = self.get(alert_id)
        if alert is None:
            return False

        if reason is not None and len(reason) > 0:
            alert.reason = reason

        if timestamp is not None:
            alert.timestamp = self.get_time_from_string_timestamp(timestamp)

        DBConnector.session.add(alert)
        self.connector.session.commit()
        return True

    def update_alert__fully(self, alert_id, reason, timestamp):
        alert: Alert = self.get(alert_id)
        if alert is None:
            return False

        alert.reason = reason
        alert.timestamp = self.get_time_from_string_timestamp(timestamp)

        DBConnector.session.add(alert)
        self.connector.session.commit()
        return True

    @staticmethod
    def get_time_from_string_timestamp(timestamp_string: str):
        return datetime.strptime(timestamp_string, '%Y-%m-%dT%H:%M:%S')
