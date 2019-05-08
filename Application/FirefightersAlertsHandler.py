from tornado.web import HTTPError
from Application.MyBaseHandler import MyBaseHandler
from Controllers.FirefightersAlertsController import FirefightersAlertsController
from Exceptions.Exceptions import ObjectAlreadyExistsInCollectionException, ObjectNotFoundInCollectionException, \
    ObjectNotFoundInDBException


class FirefightersAlertsHandler(MyBaseHandler):
    def get(self, firefighter_id="", alert_id=""):
        if len(firefighter_id) > 0:
            self.set_header('Content-Type', 'application/json')
            controller = FirefightersAlertsController()
            try:
                if len(alert_id) > 0:
                    self.write(controller.get_alert_info(int(firefighter_id), int(alert_id)))
                else:
                    self.write(controller.get_firefighter_alerts_info(int(firefighter_id)))
            except ValueError:
                raise HTTPError(405)
            except ObjectNotFoundInDBException:
                raise HTTPError(404)
        else:
            raise HTTPError(405)

    def post(self,firefighter_id="", alert_id=""):
        if len(firefighter_id) == 0 or len(alert_id) > 0:
            raise HTTPError(405)
        else:
            controller = FirefightersAlertsController()
            try:
                firefighter_id = self.get_argument("firefighter_id", "")
                controller.assign_firefighter_to_alert(int(firefighter_id), int(alert_id))
                self.set_status(201)
                self.finish()
            except ValueError:
                self.write("Incorrect parameters")
                self.set_status(403)
                self.finish()
            except ObjectAlreadyExistsInCollectionException:
                self.write("Firefighter is already assigned to this alert")
                self.set_status(403)
                self.finish()

    def delete(self, firefighter_id="", alert_id=""):
        if len(firefighter_id) > 0 and len(alert_id) > 0:
            controller = FirefightersAlertsController()
            try:
                controller.discharge_firefighter_from_alert(int(firefighter_id), int(alert_id))
                self.set_status(204)
                self.finish()
            except ValueError:
                self.write("Incorrect parameters")
                self.set_status(403)
                self.finish()
            except ObjectNotFoundInCollectionException:
                self.write("Firefighter is not assigned to this alert")
                self.set_status(403)
                self.finish()
        else:
            raise HTTPError(405)

    def patch(self, firefighter_id="", alert_id=""):
        raise HTTPError(405)

    def put(self, firefighter_id="", alert_id=""):
        raise HTTPError(405)
