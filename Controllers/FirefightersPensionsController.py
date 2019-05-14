from datetime import datetime
from sqlalchemy.orm import Session

from DAOs.DBConnector import DBConnector
from DAOs.FirefightersDAO import FirefightersDAO
from DAOs.SessionProvider import SessionProvider
from DataBaseModel import HonoraryMember
from Exceptions.Exceptions import ObjectNotFoundInDBException


class FirefightersPensionsController:
    dao: FirefightersDAO = None
    session: Session = None

    def __init__(self):
        sp = SessionProvider()
        self.session = sp.get_session()
        connector = DBConnector(self.session)
        self.dao = FirefightersDAO(connector)

    def retire_firefighter(self, firefighter_id: int) -> None:
        try:
            if isinstance(firefighter_id, int):
                firefighter_to_retire = self.dao.get(firefighter_id)
                if firefighter_to_retire.is_active is True:
                    firefighter_to_retire.is_active = False

                    honorary_member = HonoraryMember(is_active=True)
                    honorary_member.person = firefighter_to_retire.person

                    self.dao.add(honorary_member)
                    self.session.commit()
                else:
                    raise ObjectNotFoundInDBException
            else:
                raise ValueError
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()
