from typing import List

from DAOs.DBConnector import DBConnector
from DataBaseModel import Vehicle


class VehiclesDAO:
    connector = DBConnector()

    def query_all(self) -> List[Vehicle]:
        return self.connector.query_from_db(Vehicle).all()

    def get(self, vehicle_id: int) -> Vehicle:
        return self.connector.get_by_id(Vehicle, vehicle_id)

    def add(self, vehicle: Vehicle) -> None:
        try:
            self.connector.add_to_db(vehicle)
            self.connector.session.commit()
        except Exception:
            self.connector.session.rollback()
            raise

    def delete_vehicle(self, vehicle: Vehicle) -> None:
        try:
            self.connector.session.delete(vehicle)
            self.connector.session.commit()
        except Exception:
            self.connector.session.rollback()
            raise
