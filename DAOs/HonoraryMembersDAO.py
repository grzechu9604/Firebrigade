from typing import List, Optional

from sqlalchemy.orm.exc import NoResultFound

from DAOs.DBConnector import DBConnector
from DataBaseModel import HonoraryMember


class HonoraryMembersDAO:
    connector: DBConnector = None

    def __init__(self, connector: DBConnector):
        self.connector = connector

    def query_all(self) -> List[HonoraryMember]:
        return self.connector.query_from_db(HonoraryMember).all()

    def query_all_active(self) -> List[HonoraryMember]:
        return self.connector.query_from_db(HonoraryMember).filter(HonoraryMember.is_active == 1).all()

    def get(self, honorary_member_id: int) -> HonoraryMember:
        return self.connector.get_by_id(HonoraryMember, honorary_member_id)

    def add(self, honorary_member: HonoraryMember) -> None:
        self.connector.add_to_db(honorary_member)

    def get_same(self, honorary_member: HonoraryMember) -> Optional[HonoraryMember]:
        try:
            return self.connector.query_from_db(HonoraryMember)\
                    .filter(HonoraryMember.name == honorary_member.name and
                            HonoraryMember.birth_date == honorary_member.birth_date and
                            HonoraryMember.last_name == honorary_member.last_name).one()
        except NoResultFound:
            return None

    def query_page_active(self, page_no: int = 1, records_per_page: int = 10) -> List[HonoraryMember]:
        return self.connector.query_from_db(HonoraryMember).filter(HonoraryMember.is_active == 1).\
                limit(records_per_page).offset((page_no - 1) * records_per_page).all()
