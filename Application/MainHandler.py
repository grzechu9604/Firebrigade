from Application.MyBaseHandler import MyBaseHandler


class MainHandler(MyBaseHandler):
    def get(self):
        self.write("Aplikacja służy do zarządzania remizą")
