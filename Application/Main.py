import tornado.ioloop
import tornado.web

from Application.FirefightersPensionsHandler import FirefightersPensionsHandler
from Application.MainHandler import MainHandler
from Application.AlertsHandler import AlertsHandler
from Application.VehiclesHandler import VehiclesHandler
from Application.HonoraryMembersHandler import HonoraryMembersHandler
from Application.FirefightersHandler import FirefightersHandler
from Application.AlertsFirefighterHandler import AlertsFirefightersHandler
from Application.FirefightersAlertsHandler import FirefightersAlertsHandler

if __name__ == "__main__":
    handlers = [
        (r"/", MainHandler),
        (r"/firefighters[\/]{0,1}", FirefightersHandler),
        (r"/firefighters/([0-9]+)", FirefightersHandler),
        (r"/alerts[\/]{0,1}", AlertsHandler),
        (r"/alerts/([0-9]+)", AlertsHandler),
        (r"/vehicles[\/]{0,1}", VehiclesHandler),
        (r"/vehicles/([0-9]+)", VehiclesHandler),
        (r"/honoraryMembers[\/]{0,1}", HonoraryMembersHandler),
        (r"/honoraryMembers/([0-9]+)", HonoraryMembersHandler),
        (r"/alerts/([0-9]+)/firefighters[\/]{0,1}", AlertsFirefightersHandler),
        (r"/alerts/([0-9]+)/firefighters/([0-9]+)", AlertsFirefightersHandler),
        (r"/firefighters/([0-9]+)/alerts[\/]{0,1}", FirefightersAlertsHandler),
        (r"/firefighters/([0-9]+)/alerts/([0-9]+)", FirefightersAlertsHandler),
        (r"/firefightersPensions/([0-9]+)", FirefightersPensionsHandler),
    ]
    application = tornado.web.Application(handlers)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
