from datetime import datetime, date

from sqlalchemy.orm import Session

from DAOs.FirefightersDAO import FirefightersDAO
from DAOs.HonoraryMembersDAO import HonoraryMembersDAO
from DAOs.PersonsDAO import PersonsDAO
from DataBaseModel import HonoraryMember, Person
from Exceptions.Exceptions import ObjectNotFoundInDBException, ObjectExistsInDBException
from DAOs.SessionProvider import SessionProvider
from DAOs.DBConnector import DBConnector


class HonoraryMembersController:
    dao: HonoraryMembersDAO = None
    session: Session = None
    persons_dao: PersonsDAO = None

    def __init__(self):
        sp = SessionProvider()
        self.session = sp.get_session()
        connector = DBConnector(self.session)
        self.dao = HonoraryMembersDAO(connector)
        self.firefighters_dao = FirefightersDAO(connector)

    def get_honorary_member(self, honorary_member_id: int) -> HonoraryMember:
        try:
            if isinstance(honorary_member_id, int):
                return self.dao.get(honorary_member_id)
            else:
                raise ValueError
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def get_active_honorary_member(self, honorary_member_id: int) -> HonoraryMember:
        try:
            hm = self.get_honorary_member(honorary_member_id)
            if hm is not None and hm.is_active is True:
                return hm
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def get_active_honorary_member_info_in_json(self, honorary_member_id: int) -> str:
        try:
            firefighter = self.get_active_honorary_member(honorary_member_id)
            if firefighter is None:
                raise ObjectNotFoundInDBException
            else:
                return firefighter.to_full_json()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def get_honorary_member_info_in_json(self, honorary_member_id: int) -> str:
        try:
            honorary_member = self.get_honorary_member(honorary_member_id)
            if honorary_member is None:
                raise ObjectNotFoundInDBException
            else:
                return honorary_member.to_full_json()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def get_active_honorary_members_info_in_json(self) -> str:
        try:
            return str.format("[{0}]", str.join(",", [hm.to_list_json() for hm in self.dao.query_all_active()]))
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def query_page_active_honorary_members_in_list_json(self, page_no: int = 1, records_per_page: int = 10) -> str:
        try:
            members_page = self.dao.query_page_active(page_no, records_per_page) \
                if page_no > 0 else self.dao.query_all_active()
            return "[" + str.join(",", [a.to_list_json() for a in members_page]) + "]"
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def deactivate_honorary_member(self, honorary_member_id: int) -> None:
        try:
            honorary_member = self.get_honorary_member(honorary_member_id)
            if honorary_member is None or honorary_member.is_active is False:
                raise ObjectNotFoundInDBException
            else:
                honorary_member.is_active = False
                self.dao.add(honorary_member)
                self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def create_honorary_member(self, name: str, last_name: str, birth_date_str: str,
                               inactive_firefighter_id: int) -> None:
        try:
            if inactive_firefighter_id is not None:
                firefighter = self.firefighters_dao.get(int(inactive_firefighter_id))

                if firefighter is None or firefighter.is_active:
                    raise ObjectNotFoundInDBException

                person = firefighter.person

            else:
                if name is None or last_name is None or len(name) == 0 or len(last_name) == 0:
                    raise ValueError

                birth_date = None
                if birth_date_str is not None and len(birth_date_str) > 0:
                    birth_date = self.get_time_from_string_timestamp(birth_date_str)

                person = Person(name=name, last_name=last_name, birth_date=birth_date)

            honorary_member = HonoraryMember(person=person, is_active=True)
            existing_honorary_member = self.dao.get_same(honorary_member)
            if existing_honorary_member is not None:
                raise ObjectExistsInDBException(existing_honorary_member.person_id)

            self.dao.add(honorary_member)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def update_honorary_member_partially(self, honorary_member_id, name, last_name, birth_date_str) -> None:
        try:
            honorary_member = self.dao.get(honorary_member_id)
            if honorary_member is None or honorary_member.is_active is False:
                raise ObjectNotFoundInDBException

            if name is not None and len(name) > 0:
                honorary_member.person.name = name

            if last_name is not None and len(last_name) > 0:
                honorary_member.person.last_name = last_name

            if birth_date_str is not None and len(birth_date_str) > 0:
                honorary_member.person.birth_date = self.get_time_from_string_timestamp(birth_date_str)

            self.dao.add(honorary_member)
            self.session.commit()

        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def update_honorary_member_fully(self, honorary_member_id, name, last_name, birth_date_str) -> None:
        try:
            honorary_member = self.dao.get(honorary_member_id)
            if honorary_member is None or honorary_member.is_active is False:
                raise ObjectNotFoundInDBException

            if name is None or len(name) == 0 or last_name is None or len(last_name) == 0:
                raise ValueError

            if birth_date_str is not None and len(birth_date_str) > 0:
                honorary_member.person.birth_date = self.get_time_from_string_timestamp(birth_date_str)
            else:
                honorary_member.person.birth_date = None

            honorary_member.person.last_name = last_name
            honorary_member.person.name = name

            self.dao.add(honorary_member)
            self.session.commit()

        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    @staticmethod
    def get_time_from_string_timestamp(timestamp_string: str) -> date:
        return datetime.strptime(timestamp_string, '%Y-%m-%d').date()
