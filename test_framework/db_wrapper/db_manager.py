from test_framework.db_wrapper.db_connector import DBConnector
from test_framework.environments.data_base_environment import DataBaseEnvironment
from test_framework.environments.full_environment import FullEnvironment


class DBManager:
    def __init__(self, db_environment: DataBaseEnvironment = None):
        self.db_host = db_environment.db_host
        self.db_name = db_environment.db_name
        self.db_user = db_environment.db_user
        self.db_pass = db_environment.db_pass
        self.db_type = db_environment.db_type
        self.db_port = db_environment.db_port
        self.my_db = DBConnector().connect_to_db(host=self.db_host, name=self.db_name, user=self.db_user,
                                                 password=self.db_pass, db_type=self.db_type, port=self.db_port)

    def execute_query(self, query: str = None):
        out = tuple()
        self.my_db.execute(query)
        for value in self.my_db: out += (value, )
        self.my_db.close()
        return out

    def get_collection(self, collection_name):
        if self.db_type != "mongo":
            raise ValueError('Method only for mongo DB')
        return self.my_db[collection_name]

    def drop_collection(self, collection_name):
        if self.db_type != "mongo":
            raise ValueError('Method only for mongo DB')
        coll = self.get_collection(collection_name)
        if collection_name in self.my_db.list_collection_names():
            coll.drop()

    def insert_many(self, collection, data):
        if self.db_type != "mongo":
            raise ValueError('Method only for mongo DB')
        collection.insert_many(data)

    def insert_one(self, collection, data):
        if self.db_type != "mongo":
            raise ValueError('Method only for mongo DB')
        collection.insert_one(data)

    def insert_many_to_mongodb_with_drop(self, data, collection_name):
        if self.db_type != "mongo":
            raise ValueError('Method only for mongo DB')
        collection = self.get_collection(collection_name)
        self.drop_collection(collection_name)
        self.insert_many(collection, data)

    def insert_one_to_mongodb_with_drop(self, data, collection_name):
        if self.db_type != "mongo":
            raise ValueError('Method only for mongo DB')
        collection = self.get_collection(collection_name)
        self.drop_collection(collection_name)
        self.insert_one(collection, data)

    def create_empty_collection(self, collection_name):
        self.insert_many_to_mongodb_with_drop({},collection_name)