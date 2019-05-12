from tornado.web import HTTPError

from Controllers.HonoraryMembersController import HonoraryMembersController
from Application.MyBaseHandler import MyBaseHandler
from Exceptions.Exceptions import ObjectNotFoundInDBException, ObjectExistsInDBException


class HonoraryMembersHandler(MyBaseHandler):
    def get(self, honorary_member_id=""):
        controller = HonoraryMembersController()
        try:
            response = controller.get_active_honorary_member_info_in_json(int(honorary_member_id)) \
                if len(honorary_member_id) > 0 else controller.get_active_honorary_members_info_in_json()

            self.set_header('Content-Type', 'application/json')
            self.write(response)
            self.set_status(200)
            self.finish()
        except ValueError:
            raise HTTPError(405)
        except ObjectNotFoundInDBException:
            raise HTTPError(404)

    def post(self, honorary_member_id=""):
        if len(honorary_member_id) > 0:
            raise HTTPError(405)
        else:
            controller = HonoraryMembersController()
            try:
                controller.create_honorary_member(self.get_argument("name"),
                                                  self.get_argument("last_name"),
                                                  self.get_argument("birth_date", None))

                self.set_status(201)
                self.finish()
            except ValueError:
                raise HTTPError(405)
            except ObjectExistsInDBException:
                raise HTTPError(303)

    def put(self, honorary_member_id=""):
        if len(honorary_member_id) == 0:
            raise HTTPError(405)
        else:
            controller = HonoraryMembersController()
            try:
                controller.update_honorary_member_fully(int(honorary_member_id), self.get_argument("name"),
                                                        self.get_argument("last_name"),
                                                        self.get_argument("birth_date", None))

                self.set_status(200)
                self.finish()
            except ValueError:
                raise HTTPError(405)
            except ObjectNotFoundInDBException:
                raise HTTPError(404)

    def patch(self, honorary_member_id=""):
        if len(honorary_member_id) == 0:
            raise HTTPError(405)
        else:
            controller = HonoraryMembersController()
            try:
                controller.update_honorary_member_partially(int(honorary_member_id), self.get_argument("name", None),
                                                            self.get_argument("last_name", None),
                                                            self.get_argument("birth_date", None))

                self.set_status(200)
                self.finish()
            except ValueError:
                raise HTTPError(405)
            except ObjectNotFoundInDBException:
                raise HTTPError(404)

    def delete(self, honorary_member_id=""):
        if len(honorary_member_id) == 0:
            raise HTTPError(405)
        else:
            controller = HonoraryMembersController()
            try:
                controller.deactivate_honorary_member(int(honorary_member_id))
                self.set_status(204)
                self.finish()
            except ValueError:
                raise HTTPError(405)
            except ObjectNotFoundInDBException:
                raise HTTPError(404)
