from tornado.httpclient import HTTPError
from Application.MyBaseHandler import MyBaseHandler
from Controllers.FirefightersAlertsController import FirefightersAlertsController


class AlertsFirefightersHandler(MyBaseHandler):
    def get(self, alert_id="", firefighter_id=""):
        if len(alert_id) > 0:
            if len(firefighter_id) > 0:
                self.write("AlertsFirefightersHandler GET alert_id: " + alert_id + "firefighter_id: " + firefighter_id)
            else:
                controller = FirefightersAlertsController()
                self.write(controller.get_firefighters_assigned_to_alert_info(int(alert_id)))
        else:
            raise HTTPError(405)

    def post(self, alert_id="", firefighter_id=""):
        if len(alert_id) == 0 or len(firefighter_id) > 0:
            raise HTTPError(405)
        else:
        # przypisanie strażaka do alarmu
            pass

    def delete(self, alert_id="", firefighter_id=""):
        if len(firefighter_id) > 0 and len(alert_id) > 0:
            self.write("FirefightersAlertsHandler GET firefighter_id: " + firefighter_id + "alert_id: " + alert_id)
        else:
            raise HTTPError(405)

    def patch(self, alert_id="", firefighter_id=""):
        raise HTTPError(405)

    def put(self, alert_id="", firefighter_id=""):
        raise HTTPError(405)
