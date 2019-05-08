from typing import List

from DAOs.DBConnector import DBConnector
from DataBaseModel import Alert


class AlertsDAO:
    connector = DBConnector()

    def query_all(self) -> List[Alert]:
        return self.connector.query_from_db(Alert).all()

    def get(self, alert_id: int) -> Alert:
        return self.connector.get_by_id(Alert, alert_id)

    def add(self, alert: Alert) -> None:
        try:
            self.connector.add_to_db(alert)
            self.connector.session.commit()
        except Exception:
            self.connector.session.rollback()
            raise

    def delete_alert(self, alert: Alert) -> None:
        try:
            self.connector.session.delete(alert)
            self.connector.session.commit()
        except Exception:
            self.connector.session.rollback()
            raise
