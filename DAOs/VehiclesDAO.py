from typing import List

from DAOs.DBConnector import DBConnector
from DataBaseModel import Vehicle


class VehiclesDAO:
    connector: DBConnector = None

    def __init__(self, connector: DBConnector):
        self.connector = connector

    def query_all(self) -> List[Vehicle]:
        return self.connector.query_from_db(Vehicle).all()

    def get(self, vehicle_id: int) -> Vehicle:
        return self.connector.get_by_id(Vehicle, vehicle_id)

    def add(self, vehicle: Vehicle) -> None:
        self.connector.add_to_db(vehicle)

    def delete_vehicle(self, vehicle: Vehicle) -> None:
        self.connector.session.delete(vehicle)

