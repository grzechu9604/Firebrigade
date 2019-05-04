from tornado.httpclient import HTTPError
from Application.MyBaseHandler import MyBaseHandler


class FirefightersAlertsHandler(MyBaseHandler):
    def get(self, firefighter_id="", alert_id=""):
        if len(firefighter_id) > 0:
            if len(alert_id) > 0:
                self.write("FirefightersAlertsHandler GET firefighter_id: " + firefighter_id + "alert_id: " + alert_id)
            else:
                self.write("FirefightersAlertsHandler GET firefighter_id: " + firefighter_id + "alerts list")
        else:
            raise HTTPError(405)

    def put(self):
        self.write("FirefightersAlertsHandler put")
