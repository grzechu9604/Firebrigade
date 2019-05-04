from Application.MyBaseHandler import MyBaseHandler


class MainHandler(MyBaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        self.write("Aplikacja służy do zarządzania remizą")