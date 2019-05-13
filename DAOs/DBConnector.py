from sqlalchemy.orm import query
from sqlalchemy.orm.exc import NoResultFound


class DBConnector:
    session = None

    def __init__(self, session):
        self.session = session

    def query_from_db(self, object_type) -> query:
        return self.session.query(object_type)

    def add_to_db(self, new_object):
        return self.session.add(new_object)

    def get_by_id(self, object_type, object_id):
        try:
            return self.session.query(object_type).get(int(object_id))
        except NoResultFound:
            return None
