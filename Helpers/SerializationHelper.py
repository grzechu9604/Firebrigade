import datetime
import json


class SerializationHelper:
    def to_json(self):
        return json.dumps(self, default=lambda o: o.isoformat() if isinstance(o, datetime.datetime) else o.__dict__,
                          sort_keys=True, indent=4)
