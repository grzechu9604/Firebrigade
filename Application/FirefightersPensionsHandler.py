from Controllers.FirefightersPensionsController import FirefightersPensionsController
from tornado.web import HTTPError
from Application.MyBaseHandler import MyBaseHandler
from Exceptions.Exceptions import ObjectNotFoundInDBException


class FirefightersPensionsHandler(MyBaseHandler):
    def post(self, firefighter_id: int):
        controller = FirefightersPensionsController()
        try:
            controller.retire_firefighter(int(firefighter_id))
            self.set_status(201)
            self.finish()
        except ValueError:
            raise HTTPError(405)
        except ObjectNotFoundInDBException:
            raise HTTPError(404)
