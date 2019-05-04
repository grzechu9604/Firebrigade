from tornado.web import HTTPError
from DAOs import FirefightersDAO
from Application.MyBaseHandler import MyBaseHandler


class FirefightersHandler(MyBaseHandler):
    def get(self, firefighter_id=""):
        dao = FirefightersDAO.FirefightersDAO()
        response = dao.get_full_in_json(firefighter_id) if len(firefighter_id) > 0 else dao.query_all_in_list_json()
        if response is None:
            raise HTTPError(404)
        self.write(response)

