from datetime import datetime

from DAOs.DBConnector import DBConnector
from DataBaseModel import HonoraryMember


class HonoraryMembersDAO:
    connector = DBConnector()

    def query_all(self):
        return self.connector.query_from_db(HonoraryMember).all()

    def get(self, honorary_member_id):
        return self.connector.get_by_id(HonoraryMember, honorary_member_id)

    def add(self, honorary_member):
        self.connector.add_to_db(honorary_member)

    def query_all_in_list_json(self):
        all_honorary_members = self.query_all()
        return "[" + str.join(",", [a.to_list_json() for a in all_honorary_members]) + "]"

    def get_full_in_json(self, honorary_member_id):
        honorary_member: HonoraryMember = self.get(honorary_member_id)
        if honorary_member is not None:
            return honorary_member.to_full_json()
        else:
            return None

    def deactivate_honorary_member(self, honorary_member_id):
        honorary_member: HonoraryMember = self.get(honorary_member_id)
        if honorary_member is None or honorary_member.is_active is False:
            return False
        else:
            honorary_member.is_active = False
            self.connector.session.add(honorary_member)
            self.connector.session.commit()
            return True

    def create_honorary_member(self, name, last_name, birth_date_str):
        if name is None or last_name is None or len(name) == 0 or len(last_name) == 0:
            return False

        try:
            birth_date = None
            if birth_date_str is not None and len(birth_date_str) > 0:
                birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')

            honorary_member = HonoraryMember(name=name, last_name=last_name, birth_date=birth_date, is_active=True)
            self.add(honorary_member)
            self.connector.session.commit()
            return True
        except:
            return False

    def update_honorary_member_partially(self, honorary_member_id, name, last_name, birth_date_str):
        honorary_member: HonoraryMember = self.get(honorary_member_id)
        if honorary_member is None or honorary_member.is_active is False:
            return False

        if name is not None and len(name) > 0:
            honorary_member.name = name

        if last_name is not None and len(last_name) > 0:
            honorary_member.last_name = last_name

        if birth_date_str is not None and len(birth_date_str) > 0:
            honorary_member.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')

        DBConnector.session.add(honorary_member)
        self.connector.session.commit()
        return True

    def update_honorary_member_fully(self, honorary_member_id, name, last_name, birth_date_str):
        honorary_member: HonoraryMember = self.get(honorary_member_id)
        if honorary_member is None or honorary_member.is_active is False:
            return False

        honorary_member.name = name
        honorary_member.last_name = last_name
        if birth_date_str is not None and len(birth_date_str) > 0:
            honorary_member.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
        else:
            honorary_member.birth_date = None

        DBConnector.session.add(honorary_member)
        self.connector.session.commit()
        return True
