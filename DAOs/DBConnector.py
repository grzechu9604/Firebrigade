from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from DataBaseModel import Base


class DBConnector:

    engine = create_engine('sqlite:///../fire_brigade.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    def query_from_db(self, object_type):
        return self.session.query(object_type)

    def add_to_db(self, new_object):
        return self.session.add(new_object)

    def get_by_id(self, object_type, object_id):
        try:
            return self.session.query(object_type).get(int(object_id))
        except NoResultFound:
            return None
