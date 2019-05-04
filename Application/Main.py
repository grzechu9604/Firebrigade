import tornado.ioloop
import tornado.web

from Application import MainHandler

if __name__ == "__main__":
    application = tornado.web.Application([
        ("/", MainHandler)
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
