from Application.MyBaseHandler import MyBaseHandler


class AlertsHandler(MyBaseHandler):
    def get(self, alert_id=""):
        if len(alert_id) > 0:
            self.write("AlertsHandler GET alert_id: " + alert_id)
        else:
            self.write("AlertsHandler GET lista ")

    def put(self):
        self.write("AlertsHandler put")
