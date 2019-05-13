from tornado.web import HTTPError
from Application.MyBaseHandler import MyBaseHandler
from Controllers.AlertsController import AlertsController
from Exceptions.Exceptions import ObjectNotFoundInDBException, ObjectExistsInDBException


class AlertsHandler(MyBaseHandler):
    def get(self, alert_id=""):
        controller = AlertsController()
        try:
            response = controller.get_full_in_json(int(alert_id)) \
                if len(alert_id) > 0 else \
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

    def post(self, alert_id=""):
        if len(alert_id) > 0:
            raise HTTPError(405)
        else:
            controller = AlertsController()
            try:
                controller.create_alert(self.get_argument("reason"), self.get_argument("timestamp"))

                self.set_status(201)
                self.finish()
            except ValueError:
                raise HTTPError(405)
            except ObjectExistsInDBException:
                raise HTTPError(303)

    def put(self, alert_id=""):
        if len(alert_id) == 0:
            raise HTTPError(405)
        else:
            controller = AlertsController()
            try:
                controller.update_alert_fully(int(alert_id),
                                              self.get_argument("reason"), self.get_argument("timestamp"))
                self.set_status(200)
                self.finish()
            except ValueError:
                raise HTTPError(405)
            except ObjectNotFoundInDBException:
                raise HTTPError(404)


    def patch(self, alert_id=""):
        if len(alert_id) == 0:
            raise HTTPError(405)
        else:
            controller = AlertsController()
            try:
                controller.update_alert_partially(int(alert_id), self.get_argument("reason", None),
                                                  self.get_argument("timestamp", None))
                self.set_status(200)
                self.finish()
            except ValueError:
                raise HTTPError(405)
            except ObjectNotFoundInDBException:
                raise HTTPError(404)

    def delete(self, alert_id=""):
        if len(alert_id) == 0:
            raise HTTPError(405)
        else:
            controller = AlertsController()
            try:
                controller.delete_alert(int(alert_id))
                self.set_status(204)
                self.finish()
            except ValueError:
                raise HTTPError(405)
            except ObjectNotFoundInDBException:
                raise HTTPError(404)
