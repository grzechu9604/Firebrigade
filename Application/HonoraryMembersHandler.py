import tornado


class HonoraryMembersHandler(tornado.web.RequestHandler):
    @tornado.web.removeslash
    def get(self, member_id=""):
        if len(member_id) > 0:
            self.write("HonoraryMembersHandler GET member_id: " + member_id)
        else:
            self.write("HonoraryMembersHandler GET lista ")

    def put(self):
        self.write("HonoraryMembersHandler put")
