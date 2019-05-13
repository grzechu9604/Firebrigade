from tornado.web import HTTPError
from Application.MyBaseHandler import MyBaseHandler
from Controllers.VehiclesController import VehiclesController
from Exceptions.Exceptions import ObjectNotFoundInDBException, ObjectExistsInDBException


class VehiclesHandler(MyBaseHandler):
    def get(self, vehicle_id=""):
        controller = VehiclesController()
        try:
            response = controller.get_full_in_json(int(vehicle_id)) \
                if len(vehicle_id)  > 0 else \
                controller.query_page_in_list_json(
                    int(self.get_argument("page_no", 1)),
                    int(self.get_argument("records_per_page", 10)))

            self.set_header('Content-Type', 'application/json')
            self.write(response)
            self.set_status(200)
            self.finish()
        except ValueError:
            raise HTTPError(405)
        except ObjectNotFoundInDBException:
            raise HTTPError(404)

    def post(self, vehicle_id=""):
        if len(vehicle_id) > 0:
            raise HTTPError(405)
        else:
            controller = VehiclesController()
            try:
                controller.create_vehicle(self.get_argument("type"), self.get_argument("name"),
                                          self.get_argument("description"), self.get_argument("seats_amount"))

                self.set_status(201)
                self.finish()
            except ValueError:
                raise HTTPError(405)
            except ObjectExistsInDBException:
                raise HTTPError(303)

    def put(self, vehicle_id=""):
        if len(vehicle_id) == 0:
            raise HTTPError(405)
        else:
            controller = VehiclesController()
            try:
                controller.update_vehicle_fully(int(vehicle_id), self.get_argument("type"), self.get_argument("name"),
                                                self.get_argument("description"), self.get_argument("seats_amount"))

                self.set_status(200)
                self.finish()
            except ValueError:
                raise HTTPError(405)
            except ObjectNotFoundInDBException:
                raise HTTPError(404)

    def patch(self, vehicle_id=""):
        if len(vehicle_id) == 0:
            raise HTTPError(405)
        else:
            controller = VehiclesController()
            try:
                controller.update_vehicle_partially(int(vehicle_id), self.get_argument("type", None),
                                                   self.get_argument("name", None),
                                                   self.get_argument("description", None),
                                                   self.get_argument("seats_amount", None))
                self.set_status(200)
                self.finish()
            except ValueError:
                raise HTTPError(405)
            except ObjectNotFoundInDBException:
                raise HTTPError(404)

    def delete(self, vehicle_id=""):
        if len(vehicle_id) == 0:
            raise HTTPError(405)
        else:
            controller = VehiclesController()
            try:
                controller.delete_vehicle(int(vehicle_id))
                self.set_status(204)
                self.finish()
            except ValueError:
                raise HTTPError(405)
            except ObjectNotFoundInDBException:
                raise HTTPError(404)
