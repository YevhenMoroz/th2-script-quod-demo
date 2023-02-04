from test_framework.db_wrapper.db_connector import DBConnector
from test_framework.environments.full_environment import FullEnvironment


class DBManager:
    def __init__(self, db_environment: FullEnvironment = None):
        self.db_host = db_environment.get_list_data_base_environment()[0].db_host
        self.db_name = db_environment.get_list_data_base_environment()[0].db_name
        self.db_user = db_environment.get_list_data_base_environment()[0].db_user
        self.db_pass = db_environment.get_list_data_base_environment()[0].db_pass
        self.db_type = db_environment.get_list_data_base_environment()[0].db_type
        self.my_db = DBConnector().connect_to_db(host=self.db_host, name=self.db_name, user=self.db_user,
                                                 password=self.db_pass, db_type=self.db_type)

    def execute_query(self, query: str = None):
        out = tuple()
        self.my_db.execute(query)
        for value in self.my_db: out += (value, )
        self.my_db.close()
        return out