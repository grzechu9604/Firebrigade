from tornado.web import HTTPError

from Controllers.FirefightersController import FirefightersController
from Application.MyBaseHandler import MyBaseHandler
from Exceptions.Exceptions import ObjectNotFoundInDBException, ObjectExistsInDBException


class FirefightersHandler(MyBaseHandler):
    def get(self, firefighter_id=""):
        controller = FirefightersController()
        try:
            response = controller.get_active_firefighter_info_in_json(int(firefighter_id)) \
                if len(firefighter_id) > 0 else controller.get_active_firefighters_info_in_json()

            self.set_header('Content-Type', 'application/json')
            self.write(response)
            self.set_status(200)
            self.finish()
        except ValueError:
            raise HTTPError(405)
        except ObjectNotFoundInDBException:
            raise HTTPError(404)

    def post(self, firefighter_id=""):
        if len(firefighter_id) > 0:
            raise HTTPError(405)
        else:
            controller = FirefightersController()
            try:
                controller.create_firefighter(self.get_argument("name"),
                                              self.get_argument("last_name"),
                                              self.get_argument("birth_date", None))

                self.set_status(201)
                self.finish()
            except ValueError:
                raise HTTPError(405)
            except ObjectExistsInDBException:
                raise HTTPError(303)

    def put(self, firefighter_id=""):
        if len(firefighter_id) == 0:
            raise HTTPError(405)
        else:
            controller = FirefightersController()
            try:
                controller.update_firefighter_fully(int(firefighter_id), self.get_argument("name"),
                                                    self.get_argument("last_name"),
                                                    self.get_argument("birth_date", None))

                self.set_status(200)
                self.finish()
            except ValueError:
                raise HTTPError(405)
            except ObjectNotFoundInDBException:
                raise HTTPError(404)

    def patch(self, firefighter_id=""):
        if len(firefighter_id) == 0:
            raise HTTPError(405)
        else:
            controller = FirefightersController()
            try:
                controller.update_firefighter_partially(int(firefighter_id), self.get_argument("name", None),
                                                        self.get_argument("last_name", None),
                                                        self.get_argument("birth_date", None))

                self.set_status(200)
                self.finish()
            except ValueError:
                raise HTTPError(405)
            except ObjectNotFoundInDBException:
                raise HTTPError(404)

    def delete(self, firefighter_id=""):
        if len(firefighter_id) == 0:
            raise HTTPError(405)
        else:
            controller = FirefightersController()
            try:
                controller.deactivate_firefighter(int(firefighter_id))
                self.set_status(204)
                self.finish()
            except ValueError:
                raise HTTPError(405)
            except ObjectNotFoundInDBException:
                raise HTTPError(404)
