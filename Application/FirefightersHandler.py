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
            #dodanie strażaka
            raise NotImplemented

    def put(self, firefighter_id=""):
        if len(firefighter_id) == 0:
            raise HTTPError(405)
        else:
            #edycja strażaka jeżeli istniał
            raise NotImplemented

    def patch(self, firefighter_id=""):
        if len(firefighter_id) == 0:
            raise HTTPError(405)
        else:
            #edycja strażaka jeżeli istniał
            raise NotImplemented

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
