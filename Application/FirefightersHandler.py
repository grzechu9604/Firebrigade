import tornado


class FirefightersHandler(tornado.web.RequestHandler):
    @tornado.web.removeslash
    def get(self, firefighter_id=""):
        if len(firefighter_id) > 0:
            self.write("FirefightersHandler GET Firefighter id: " + firefighter_id)
        else:
            self.write("FirefightersHandler GET lista ")

    def put(self):
        self.write("FirefightersHandler put")
