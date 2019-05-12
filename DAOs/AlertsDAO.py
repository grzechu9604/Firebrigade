from typing import List, Optional

from sqlalchemy.orm.exc import NoResultFound

from DAOs.DBConnector import DBConnector
from DataBaseModel import Alert


class AlertsDAO:
    connector: DBConnector = None

    def __init__(self, connector: DBConnector):
        self.connector = connector

    def query_all(self) -> List[Alert]:
        return self.connector.query_from_db(Alert).all()

    def get(self, alert_id: int) -> Alert:
        return self.connector.get_by_id(Alert, alert_id)

    def add(self, alert: Alert) -> None:
        self.connector.add_to_db(alert)

    def delete_alert(self, alert: Alert) -> None:
        self.connector.session.delete(alert)

    def get_same(self, alert: Alert) -> Optional[Alert]:
        try:
            return self.connector.query_from_db(Alert)\
                    .filter(Alert.reason == alert.reason and
                            Alert.timestamp == alert.timestamp).one()
        except NoResultFound:
            return None
