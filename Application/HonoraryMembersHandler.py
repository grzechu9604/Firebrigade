from Application.MyBaseHandler import MyBaseHandler


class HonoraryMembersHandler(MyBaseHandler):
    def get(self, member_id=""):
        if len(member_id) > 0:
            self.write("HonoraryMembersHandler GET member_id: " + member_id)
        else:
            self.write("HonoraryMembersHandler GET lista ")

    def put(self):
        self.write("HonoraryMembersHandler put")
