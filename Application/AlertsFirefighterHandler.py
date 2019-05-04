import tornado
from tornado.httpclient import HTTPError
from Application.MyBaseHandler import MyBaseHandler


class AlertsFirefightersHandler(MyBaseHandler):
    def get(self, alert_id="", firefighter_id=""):
        if len(alert_id) > 0:
            if len(firefighter_id) > 0:
                self.write("AlertsFirefightersHandler GET alert_id: " + alert_id + "firefighter_id: " + firefighter_id)
            else:
                self.write("AlertsFirefightersHandler GET alert_id: " + alert_id + "firefighters list")
        else:
            raise HTTPError(405)

    def put(self):
        self.write("AlertsFirefightersHandler put")
