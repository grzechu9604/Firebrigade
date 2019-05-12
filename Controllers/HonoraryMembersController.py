from datetime import datetime

from sqlalchemy.orm import Session
from DAOs.HonoraryMembersDAO import HonoraryMembersDAO
from DataBaseModel import HonoraryMember
from Exceptions.Exceptions import ObjectNotFoundInDBException
from DAOs.SessionProvider import SessionProvider
from DAOs.DBConnector import DBConnector


class HonoraryMembersController:
    dao: HonoraryMembersDAO = None
    session: Session = None

    def __init__(self):
        sp = SessionProvider()
        self.session = sp.get_session()
        connector = DBConnector(self.session)
        self.dao = HonoraryMembersDAO(connector)

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

    def deactivate_honorary_member(self, honorary_member_id: int) -> None:
        try:
            honorary_member = self.get_honorary_member(honorary_member_id)
            if honorary_member is None:
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

    def create_honorary_member(self, name: str, last_name: str, birth_date_str: str) -> None:
        try:
            if name is None or last_name is None or len(name) == 0 or len(last_name) == 0:
                raise ValueError

            birth_date = None
            if birth_date_str is not None and len(birth_date_str) > 0:
                birth_date = self.get_time_from_string_timestamp(birth_date_str)

            honorary_member = HonoraryMember(name=name, last_name=last_name, birth_date=birth_date, is_active=True)
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
                honorary_member.name = name

            if last_name is not None and len(last_name) > 0:
                honorary_member.last_name = last_name

            if birth_date_str is not None and len(birth_date_str) > 0:
                honorary_member.birth_date = self.get_time_from_string_timestamp(birth_date_str)

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
                honorary_member.birth_date = self.get_time_from_string_timestamp(birth_date_str)
            else:
                honorary_member.birth_date = None

            honorary_member.last_name = last_name
            honorary_member.name = name

            self.dao.add(honorary_member)
            self.session.commit()

        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    @staticmethod
    def get_time_from_string_timestamp(timestamp_string: str) -> datetime:
        return datetime.strptime(timestamp_string, '%Y-%m-%d')
