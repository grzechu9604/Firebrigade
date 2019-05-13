from typing import List, Optional

from sqlalchemy.orm.exc import NoResultFound

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

    def get_same(self, vehicle: Vehicle) -> Optional[Vehicle]:
        try:
            return self.connector.query_from_db(Vehicle)\
                    .filter(Vehicle.seats_amount == vehicle.seats_amount and
                            Vehicle.name == vehicle.name and
                            Vehicle.description == vehicle.description and
                            Vehicle.type == vehicle.type).one()
        except NoResultFound:
            return None

    def query_page(self, page_no: int = 1, records_per_page: int = 10) -> List[Vehicle]:
        return self.connector.query_from_db(Vehicle).limit(records_per_page)\
            .offset((page_no - 1) * records_per_page).all()
