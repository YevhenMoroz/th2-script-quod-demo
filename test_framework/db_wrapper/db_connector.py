import psycopg2 as postgresql
import oracledb as oracle
import pymongo

class DBConnector:

    def connect_to_db(self, host, name, user, password, db_type, port):
        try:

            if db_type.lower() == 'postgresql':
                mydb = postgresql.connect(host=host, database=name, user=user, password=password)
                mydb.autocommit = True
                return mydb.cursor()

            if db_type.lower() == 'oracle':
                """
                A cursor will be closed automatically when the variable referencing it goes out of scope 
                (and no further references are retained). A "with" block is a convenient way to ensure this
                """
                mydb = oracle.connect(dsn=f"{host}/{name}", user=user, password=password)
                with mydb.cursor():
                    return mydb.cursor()

            if db_type.lower() == 'mongo':
                client = pymongo.MongoClient(host, port)
                return client[name]

        except Exception as e:
            print(f"!!!!!DB connection could not be established!!!!!: {e}")