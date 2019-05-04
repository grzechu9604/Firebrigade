import tornado
import json


class MyBaseHandler(tornado.web.RequestHandler):

    def write_error(self, status_code, **kwargs):
        self.set_header('Content-Type', 'application/json')
        self.finish(json.dumps({
            'error': {
                'code': status_code,
                'message': self._reason
            }
        }))
