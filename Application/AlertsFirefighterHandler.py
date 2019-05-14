from tornado.web import HTTPError
from Application.MyBaseHandler import MyBaseHandler
from Controllers.FirefightersAlertsController import FirefightersAlertsController
from Exceptions.Exceptions import ObjectAlreadyExistsInCollectionException, ObjectNotFoundInDBException, \
    ObjectNotFoundInCollectionException


class AlertsFirefightersHandler(MyBaseHandler):
    def get(self, alert_id="", firefighter_id=""):
        if len(alert_id) > 0:
            self.set_header('Content-Type', 'application/json')
            controller = FirefightersAlertsController()
            try:
                if len(firefighter_id) > 0:
                    self.write(controller.get_firefighter_info(int(alert_id), int(firefighter_id)))
                else:
                    self.write(controller.get_firefighters_assigned_to_alert_info(int(alert_id)))
            except ValueError:
                raise HTTPError(405)
            except ObjectNotFoundInDBException:
                raise HTTPError(404)
        else:
            raise HTTPError(405)

    def post(self, alert_id="", firefighter_id=""):
        if len(alert_id) == 0 or len(firefighter_id) > 0:
            raise HTTPError(405)
        else:
            controller = FirefightersAlertsController()
            try:
                firefighter_id = self.get_argument("firefighter_id", "")
                controller.assign_firefighter_to_alert(int(firefighter_id), int(alert_id))
                self.set_status(201)
                self.finish()
            except ValueError:
                raise HTTPError(400)
            except ObjectAlreadyExistsInCollectionException:
                raise HTTPError(303)
            except ObjectNotFoundInDBException:
                raise HTTPError(404)

    def delete(self, alert_id="", firefighter_id=""):
        if len(firefighter_id) > 0 and len(alert_id) > 0:
            controller = FirefightersAlertsController()
            try:
                controller.discharge_firefighter_from_alert(int(firefighter_id), int(alert_id))
                self.set_status(204)
                self.finish()
            except ValueError:
                raise HTTPError(400)
            except ObjectNotFoundInCollectionException:
                raise HTTPError(404)
            except ObjectNotFoundInDBException:
                raise HTTPError(404)
        else:
            raise HTTPError(405)

    def patch(self, alert_id="", firefighter_id=""):
        raise HTTPError(405)

    def put(self, alert_id="", firefighter_id=""):
        raise HTTPError(405)
