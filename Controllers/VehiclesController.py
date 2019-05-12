from DAOs.VehiclesDAO import VehiclesDAO
from DataBaseModel import Vehicle
from Exceptions.Exceptions import ObjectNotFoundInDBException
from sqlalchemy.orm import Session
from DAOs.DBConnector import DBConnector
from DAOs.SessionProvider import SessionProvider


class VehiclesController:
    dao: VehiclesDAO = None
    session: Session = None

    def __init__(self):
        sp = SessionProvider()
        self.session = sp.get_session()
        connector = DBConnector(self.session)
        self.dao = VehiclesDAO(connector)

    def get_vehicle(self, vehicle_id: int) -> Vehicle:
        if isinstance(vehicle_id, int):
            return self.dao.get(vehicle_id)
        else:
            raise ValueError

    def query_all_in_list_json(self) -> str:
        all_vehicles = self.dao.query_all()
        return "[" + str.join(",", [a.to_list_json() for a in all_vehicles]) + "]"

    def get_full_in_json(self, vehicle_id: int) -> str:
        vehicle: Vehicle = self.get_vehicle(vehicle_id)
        if vehicle is None:
            raise ObjectNotFoundInDBException
        else:
            return vehicle.to_full_json()

    def delete_vehicle(self, vehicle_id: int) -> None:
        try:
            vehicle = self.dao.get(vehicle_id)
            if vehicle is None:
                raise ObjectNotFoundInDBException

            self.dao.delete_vehicle(vehicle)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def create_vehicle(self, vehicle_type: str, name: str, description: str, seats_amount: str) -> None:
        if vehicle_type is None or name is None or description is None or seats_amount is None \
                or len(vehicle_type) == 0 or len(name) == 0 or len(description) == 0 or len(seats_amount) == 0\
                or not str.isnumeric(seats_amount) \
                or int(seats_amount) <= 0:
            raise ValueError

        vehicle = Vehicle(type=vehicle_type, name=name, description=description, seats_amount=int(seats_amount))
        try:
            self.dao.add(vehicle)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def update_vehicle_partially(self, vehicle_id: int, vehicle_type: str, name: str, description: str,
                                 seats_amount: str) -> None:
        try:
            vehicle: Vehicle = self.dao.get(vehicle_id)
            if vehicle is None:
                raise ObjectNotFoundInDBException

            if vehicle_type is not None and len(vehicle_type) > 0:
                vehicle.type = vehicle_type

            if name is not None and len(name) > 0:
                vehicle.name = name

            if description is not None and len(description) > 0:
                vehicle.description = description

            if seats_amount is not None and str.isalnum(seats_amount) and int(seats_amount) > 0:
                vehicle.seats_amount = int(seats_amount)

            self.dao.add(vehicle)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def update_vehicle_fully(self, vehicle_id: int, vehicle_type: str, name: str, description: str,
                             seats_amount: str) -> None:
        try:
            vehicle: Vehicle = self.dao.get(vehicle_id)
            if vehicle is None:
                raise ObjectNotFoundInDBException

            if vehicle_type is None or len(vehicle_type) == 0 or name is None or len(name) == 0\
                    or description is None or len(description) == 0 or seats_amount is None \
                    or not str.isalnum(seats_amount) or int(seats_amount) <= 0:
                raise ValueError

            vehicle.type = vehicle_type
            vehicle.name = name
            vehicle.description = description
            vehicle.seats_amount = int(seats_amount)

            self.dao.add(vehicle)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()
