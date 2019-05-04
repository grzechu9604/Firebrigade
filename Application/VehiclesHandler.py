from Application.MyBaseHandler import MyBaseHandler


class VehiclesHandler(MyBaseHandler):
    def get(self, vehicle_id=""):
        if len(vehicle_id) > 0:
            self.write("VehiclesHandler GET vehicle_id: " + vehicle_id)
        else:
            self.write("VehiclesHandler GET lista ")

    def put(self):
        self.write("VehiclesHandler put")
