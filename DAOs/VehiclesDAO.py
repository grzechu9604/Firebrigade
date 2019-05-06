from DAOs.DBConnector import DBConnector
from DataBaseModel import Vehicle


class VehiclesDAO:
    connector = DBConnector()

    def query_all(self):
        return self.connector.query_from_db(Vehicle).all()

    def get(self, vehicle_id):
        return self.connector.get_by_id(Vehicle, vehicle_id)

    def add(self, vehicle):
        self.connector.add_to_db(vehicle)

    def query_all_in_list_json(self):
        all_vehicles = self.query_all()
        return "[" + str.join(",", [a.to_list_json() for a in all_vehicles]) + "]"

    def get_full_in_json(self, vehicle_id):
        vehicle: Vehicle = self.get(vehicle_id)
        if vehicle is not None:
            return vehicle.to_full_json()
        else:
            return None

    def delete_vehicle(self, vehicle_id):
        vehicle: Vehicle = self.get(vehicle_id)
        if vehicle is None:
            return False
        else:
            self.connector.session.delete(vehicle)
            self.connector.session.commit()
            return True

    def create_vehicle(self, type, name, description, seats_amount):
        if type is None or name is None or description is None or seats_amount is None \
                or len(type) == 0 or len(name) == 0 or len(description) == 0 or len(seats_amount) == 0\
                or not str.isalnum(seats_amount) \
                or int(seats_amount) <= 0:
            return False

        try:
            vehicle = Vehicle(type=type, name=name, description=description, seats_amount=int(seats_amount))
            self.add(vehicle)
            self.connector.session.commit()
            return True
        except:
            return False

    def update_vehicle_partially(self, vehicle_id, type, name, description, seats_amount):
        vehicle: Vehicle = self.get(vehicle_id)
        if vehicle is None:
            return False

        if type is not None and len(type) > 0:
            vehicle.type = type

        if name is not None and len(name) > 0:
            vehicle.name = name

        if description is not None and len(description) > 0:
            vehicle.description = description

        if seats_amount is not None and str.isalnum(seats_amount) and int(seats_amount) > 0:
            vehicle.seats_amount = int(seats_amount)

        DBConnector.session.add(vehicle)
        self.connector.session.commit()
        return True

    def update_vehicle_fully(self, vehicle_id, type, name, description, seats_amount):
        vehicle: Vehicle = self.get(vehicle_id)
        if vehicle is None or type is None or len(type) == 0 or name is None or len(name) == 0\
                or description is None or len(description) == 0 or seats_amount is None \
                or not str.isalnum(seats_amount) or int(seats_amount) <= 0:
            return False

        vehicle.type = type
        vehicle.name = name
        vehicle.description = description
        vehicle.seats_amount = int(seats_amount)

        DBConnector.session.add(vehicle)
        self.connector.session.commit()
        return True
