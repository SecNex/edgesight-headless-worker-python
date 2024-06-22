import sys

import psycopg2

class Database:
    def __init__(self, host: str = "localhost", port: int = 5432, database: str = "postgres", user: str = "postgres", password: str = "postgres"):
        self.__host = host
        self.__port = port
        self.__database = database
        self.__user = user
        self.__password = password
        self.cnx = self.connect()
        self.cursor = self.cnx.cursor()

    def __del__(self):
        self.close()

    @property
    def connected(self):
        return self.cnx.status == psycopg2.extensions.STATUS_READY

    def connect(self):
        print(f"[DATABASE] Connecting to {self.__database}@{self.__host} as {self.__user}...")
        return psycopg2.connect(
            host=self.__host,
            port=self.__port,
            database=self.__database,
            user=self.__user,
            password=self.__password
        )
    
    def init(self):
        self.execute("CREATE TABLE IF NOT EXISTS websites (id SERIAL PRIMARY KEY, url TEXT, timeout INT, delay BOOLEAN, delay_time INT)")
        self.execute("CREATE TABLE IF NOT EXISTS screenshots (id SERIAL PRIMARY KEY, website_id INT, path TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        self.execute("CREATE TABLE IF NOT EXISTS logs (id SERIAL PRIMARY KEY, website_id INT, message TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

    def clear(self):
        self.execute("DROP TABLE IF EXISTS websites")
        self.execute("DROP TABLE IF EXISTS screenshots")
        self.execute("DROP TABLE IF EXISTS logs")

    def execute(self, query: str, values: tuple = ()):
        self.cursor.execute(query, values)
        self.cnx.commit()

    def fetch(self, query: str):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.cnx.close()

    def count(self, table: str):
        return self.fetch("SELECT COUNT(*) FROM %s" % table)[0][0]
            
    def test(self):
        res = self.fetch("SELECT 1")
        if res:
            print("[DATABASE] Database connection successful!")
        else:
            print("[DATABASE] Database connection failed!")
            sys.exit(1)
