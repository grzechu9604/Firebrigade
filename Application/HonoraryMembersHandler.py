from tornado.web import HTTPError
from DAOs import HonoraryMembersDAO
from Application.MyBaseHandler import MyBaseHandler


class HonoraryMembersHandler(MyBaseHandler):
    def get(self, honorary_member_id=""):
        dao = HonoraryMembersDAO.HonoraryMembersDAO()
        response = dao.get_full_in_json(honorary_member_id) if len(honorary_member_id) > 0 else dao.query_all_in_list_json()
        if response is None:
            raise HTTPError(404)

        self.set_header('Content-Type', 'application/json')
        self.write(response)

    def post(self, honorary_member_id=""):
        if len(honorary_member_id) > 0:
            raise HTTPError(405)
        else:
            dao = HonoraryMembersDAO.HonoraryMembersDAO()
            success = dao.create_honorary_member(self.get_argument("name"), self.get_argument("last_name"),
                                                 self.get_argument("birth_date", None))
            if success:
                self.set_status(201)
                self.finish()
            else:
                raise HTTPError(403)

    def put(self, honorary_member_id=""):
        if len(honorary_member_id) == 0:
            raise HTTPError(405)
        else:
            dao = HonoraryMembersDAO.HonoraryMembersDAO()
            success = dao.update_honorary_member_fully(honorary_member_id, self.get_argument("name"),
                                                       self.get_argument("last_name"),
                                                       self.get_argument("birth_date", None))
            if success:
                self.set_status(200)
                self.finish()
            else:
                raise HTTPError(404)

    def patch(self, honorary_member_id=""):
        if len(honorary_member_id) == 0:
            raise HTTPError(405)
        else:
            dao = HonoraryMembersDAO.HonoraryMembersDAO()
            success = dao.update_honorary_member_partially(honorary_member_id, self.get_argument("name", None),
                                                           self.get_argument("last_name", None),
                                                           self.get_argument("birth_date", None))
            if success:
                self.set_status(200)
                self.finish()
            else:
                raise HTTPError(404)

    def delete(self, honorary_member_id=""):
        if len(honorary_member_id) == 0:
            raise HTTPError(405)
        else:
            dao = HonoraryMembersDAO.HonoraryMembersDAO()
            success = dao.deactivate_honorary_member(honorary_member_id)
            if success:
                self.set_status(204)
                self.finish()
            else:
                raise HTTPError(404)
