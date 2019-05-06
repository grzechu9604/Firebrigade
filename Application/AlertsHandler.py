from tornado.web import HTTPError
from Application.MyBaseHandler import MyBaseHandler
from DAOs import AlertsDAO


class AlertsHandler(MyBaseHandler):
    def get(self, alert_id=""):
        dao = AlertsDAO.AlertsDAO()
        response = dao.get_full_in_json(alert_id) if len(alert_id) > 0 else dao.query_all_in_list_json()
        if response is None:
            raise HTTPError(404)

        self.set_header('Content-Type', 'application/json')
        self.write(response)

    def post(self, alert_id=""):
        if len(alert_id) > 0:
            raise HTTPError(405)
        else:
            dao = AlertsDAO.AlertsDAO()
            success = dao.create_alert(self.get_argument("reason"), self.get_argument("timestamp"))
            if success:
                self.set_status(201)
                self.finish()
            else:
                raise HTTPError(403)

    def put(self, alert_id=""):
        if len(alert_id) == 0:
            raise HTTPError(405)
        else:
            dao = AlertsDAO.AlertsDAO()
            success = dao.update_alert__fully(alert_id, self.get_argument("reason"), self.get_argument("timestamp"))

            if success:
                self.set_status(200)
                self.finish()
            else:
                raise HTTPError(404)

    def patch(self, alert_id=""):
        if len(alert_id) == 0:
            raise HTTPError(405)
        else:
            dao = AlertsDAO.AlertsDAO()
            success = dao.update_alert_partially(alert_id, self.get_argument("reason", None),
                                                 self.get_argument("timestamp", None))
            if success:
                self.set_status(200)
                self.finish()
            else:
                raise HTTPError(404)

    def delete(self, alert_id=""):
        if len(alert_id) == 0:
            raise HTTPError(405)
        else:
            dao = AlertsDAO.AlertsDAO()
            success = dao.delete_alert(alert_id)
            if success:
                self.set_status(204)
                self.finish()
            else:
                raise HTTPError(404)
