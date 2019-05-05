import json
from tornado import web


class MyBaseHandler(web.RequestHandler):

    def write_error(self, status_code, **kwargs):
        self.set_header('Content-Type', 'application/json')
        self.finish(json.dumps({
            'error': {
                'code': status_code,
                'message': self._reason
            }
        }))
