from datetime import datetime
from typing import List

from DAOs.DBConnector import DBConnector
from DataBaseModel import HonoraryMember


class HonoraryMembersDAO:
    connector = DBConnector()

    def query_all(self) -> List[HonoraryMember]:
        return self.connector.query_from_db(HonoraryMember).all()

    def query_all_active(self) -> List[HonoraryMember]:
        return self.connector.query_from_db(HonoraryMember).filter(HonoraryMember.is_active == 1).all()

    def get(self, honorary_member_id: int) -> HonoraryMember:
        return self.connector.get_by_id(HonoraryMember, honorary_member_id)

    def add(self, honorary_member: HonoraryMember) -> None:
        try:
            self.connector.add_to_db(honorary_member)
            self.connector.session.commit()
        except Exception:
            self.connector.session.rollback()
            raise

