from tornado.web import HTTPError
from Application.MyBaseHandler import MyBaseHandler
from DAOs import VehiclesDAO


class VehiclesHandler(MyBaseHandler):
    def get(self, vehicle_id=""):
        dao = VehiclesDAO.VehiclesDAO()
        response = dao.get_full_in_json(vehicle_id) if len(vehicle_id) > 0 else dao.query_all_in_list_json()
        if response is None:
            raise HTTPError(404)

        self.set_header('Content-Type', 'application/json')
        self.write(response)

    def post(self, vehicle_id=""):
        if len(vehicle_id) > 0:
            raise HTTPError(405)
        else:
            dao = VehiclesDAO.VehiclesDAO()
            success = dao.create_vehicle(self.get_argument("type"), self.get_argument("name"),
                                         self.get_argument("description"), self.get_argument("seats_amount"))
            if success:
                self.set_status(201)
                self.finish()
            else:
                raise HTTPError(403)

    def put(self, vehicle_id=""):
        if len(vehicle_id) == 0:
            raise HTTPError(405)
        else:
            dao = VehiclesDAO.VehiclesDAO()
            success = dao.update_vehicle_fully(vehicle_id, self.get_argument("type"), self.get_argument("name"),
                                               self.get_argument("description"), self.get_argument("seats_amount"))

            if success:
                self.set_status(200)
                self.finish()
            else:
                raise HTTPError(404)

    def patch(self, vehicle_id=""):
        if len(vehicle_id) == 0:
            raise HTTPError(405)
        else:
            dao = VehiclesDAO.VehiclesDAO()
            success = dao.update_vehicle_partially(vehicle_id, self.get_argument("type", None),
                                                   self.get_argument("name", None),
                                                   self.get_argument("description", None),
                                                   self.get_argument("seats_amount", None))
            if success:
                self.set_status(200)
                self.finish()
            else:
                raise HTTPError(404)

    def delete(self, vehicle_id=""):
        if len(vehicle_id) == 0:
            raise HTTPError(405)
        else:
            dao = VehiclesDAO.VehiclesDAO()
            success = dao.delete_vehicle(vehicle_id)
            if success:
                self.set_status(204)
                self.finish()
            else:
                raise HTTPError(404)
