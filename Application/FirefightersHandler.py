from tornado.web import HTTPError
from DAOs import FirefightersDAO
from Application.MyBaseHandler import MyBaseHandler


class FirefightersHandler(MyBaseHandler):
    def get(self, firefighter_id=""):
        dao = FirefightersDAO.FirefightersDAO()
        response = dao.get_full_in_json(firefighter_id) if len(firefighter_id) > 0 else dao.query_all_in_list_json()
        if response is None:
            raise HTTPError(404)

        self.set_header('Content-Type', 'application/json')
        self.write(response)

    def post(self, firefighter_id=""):
        if len(firefighter_id) > 0:
            raise HTTPError(405)
        else:
            dao = FirefightersDAO.FirefightersDAO()
            success = dao.create_firefighter(self.get_argument("name"), self.get_argument("last_name"),
                                             self.get_argument("birth_date", None))
            if success:
                self.set_status(201)
                self.finish()
            else:
                raise HTTPError(403)

    def put(self, firefighter_id=""):
        if len(firefighter_id) == 0:
            raise HTTPError(405)
        else:
            dao = FirefightersDAO.FirefightersDAO()
            success = dao.update_firefighter_fully(firefighter_id, self.get_argument("name"),
                                                   self.get_argument("last_name"),
                                                   self.get_argument("birth_date", None))
            if success:
                self.set_status(200)
                self.finish()
            else:
                raise HTTPError(404)

    def patch(self, firefighter_id=""):
        if len(firefighter_id) == 0:
            raise HTTPError(405)
        else:
            dao = FirefightersDAO.FirefightersDAO()
            success = dao.update_firefighter_partially(firefighter_id, self.get_argument("name", None),
                                                       self.get_argument("last_name", None),
                                                       self.get_argument("birth_date", None))
            if success:
                self.set_status(200)
                self.finish()
            else:
                raise HTTPError(404)

    def delete(self, firefighter_id=""):
        if len(firefighter_id) == 0:
            raise HTTPError(405)
        else:
            dao = FirefightersDAO.FirefightersDAO()
            success = dao.deactivate_firefighter(firefighter_id)
            if success:
                self.set_status(204)
                self.finish()
            else:
                raise HTTPError(404)
