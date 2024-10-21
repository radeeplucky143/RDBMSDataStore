import psycopg2
from psycopg2 import Error
from api.config import postgre_host, postgre_database, postgre_user, postgre_password
from core.SQLConnection import SQLConnection

class PostgreSQLConnection(SQLConnection):
    """ Single Responsibility Principle: establishes connection to PostgreSQL Database and execute queries"""

    def __init__(self):
        self.host = postgre_host
        self.database = postgre_database
        self.user = postgre_user
        self.password = postgre_password
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establishes a connection to the PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            print("Connected to PostgreSQL database successfully.")
            return self.cursor
        except Error as e:
            print(f"Error connecting to PostgreSQL: {e}")
            raise Exception(e)

    def commit(self):
        """Commiting the changes done in the PostgreSQL database"""
        try:
            self.connection.commit()
            print("Changes are committed to the database.")
        except Error as e:
            print(f"Error while commiting Changes to the database")
            raise Exception(e)

    def disconnect(self):
        """Closes the connection to the PostgreSQL database."""
        try:
            self.cursor.close()
            self.connection.close()
            print("Disconnected from PostgreSQL database.")
        except Error as e:
            print(f"Error disconnecting from PostgreSQL: {e}")
            raise Exception(e)
