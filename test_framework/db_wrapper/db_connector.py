import psycopg2 as postgresql
import oracledb as oracle


class DBConnector:

    def connect_to_db(self, host, name, user, password, db_type):
        try:

            if db_type.lower() == 'postgresql':
                mydb = postgresql.connect(host=host, database=name, user=user, password=password)
                return mydb.cursor()

            if db_type.lower() == 'oracle':
                mydb = oracle.connect(dsn=f"{host}/{name}", user=user, password=password)
                return mydb.cursor()

        except Exception as e:
            print(f"!!!!!DB connection could not be established!!!!!: {e}")