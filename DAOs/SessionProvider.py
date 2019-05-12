from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from DataBaseModel import Base
from Helpers.Singleton import Singleton


class SessionProvider(metaclass=Singleton):

    engine = create_engine('sqlite:///../fire_brigade.db')
    Base.metadata.bind = engine
    Session: sessionmaker = sessionmaker(bind=engine)

    def get_session(self) -> Session:
        return self.Session()
