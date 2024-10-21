from src.core.PostgreConnection import PostgreSQLConnection
from src.api.models import PostData, GetData, DeleteData
from psycopg2 import Error, OperationalError
from src.api.config import storage_limit


class DataStore:
    """ Single Responsibility Principle: Responsible for performing CRD operations on keyvalue table in datastore database"""

    def __init__(self):
        self.database = PostgreSQLConnection()
        self.cursor = self.database.connect()
        self.table_name = "keyvalue"


    def TenantStorage(self, tenant_id: str):
        """Retrieving tenant storage details"""
        try:
            sql = f"SELECT SUM(size) FROM {self.table_name} WHERE tenant_id='{tenant_id}'"
            self.cursor.execute(sql)
            results = self.cursor.fetchall()[0][0]
            return results if results else 0
        except Error as e:
            print(f"Error retrieving data: {e}")
            raise Exception(e)


    def tenantExists(self, tenant_id: str):
        """Checking whether tenant exists in the database."""
        try:
            sql = f"SELECT * FROM {self.table_name} WHERE tenant_id='{tenant_id}'"
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return True if results else False
        except Error as e:
            print(f"Error retrieving data: {e}")
            raise Exception(e)


    def RecordExists(self, tenant_id: str, key: str):
        """Checking whether record exists in the database"""
        try:
            sql = f"SELECT * FROM {self.table_name} WHERE tenant_id='{tenant_id}' AND key='{key}' AND expiry_time > CURRENT_TIMESTAMP"
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return True if results else False
        except Error as e:
            print(f"Error retrieving data: {e}")
            raise Exception(e)


    def getKey(self, object: GetData):
        """Retrieves record from a DataStore for specific (tenant_id, key).

        Args:
            object : GetData BaseModel
            tenant_id(object): id of the tenant_id
            key(object): key value user stored in the database.
        """
        try:
            sql = f"SELECT * FROM {self.table_name} WHERE key='{object.key}' AND tenant_id='{object.tenant_id}' AND expiry_time > CURRENT_TIMESTAMP"
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except Error as e:
            print(f"Error retrieving data: {e}")
            raise Exception(e)


    def deleteData(self, object: DeleteData):
        """Deletes record from a DataStore for specific (tenant_id, key).

        Args:
            object : DeleteData BaseModel
            tenant_id(object): id of the tenant_id
            key(object): key value user stored in the database..
        """
        try:
            sql = f"DELETE FROM {self.table_name} WHERE key='{object.key}' AND tenant_id='{object.tenant_id}' AND expiry_time > CURRENT_TIMESTAMP"
            self.cursor.execute(sql)
            results = self.cursor.rowcount
            if results > 0:
                self.database.commit()
                print("Record deleted successfully")
                return "Record deleted successfully."
            print("Please make sure record exists in the database before performing delete operation..")
            return "Please make sure record exists in the database before performing delete operation.."
        except Error as e:
            print(f"Error deleting data: {e}")
            raise Exception(e)


    def deleteExpired(self):
        """Deletes expired records from a DataStore database."""

        try:
            sql = f"DELETE FROM {self.table_name} WHERE expiry_time < CURRENT_TIMESTAMP"
            self.cursor.execute(sql)
            results = self.cursor.rowcount
            if results > 0:
                self.database.commit()
                return f"Total no of expiry records: {results}"
            return "No expired records found.."
        except Error as e:
            print(f"Error deleting data: {e}")
            raise Exception(e)


    def PostData(self, object: PostData):
        """Inserts record into a keyvalue table present in datastore database.

        Args:
            object : PostData BaseModel
            tenant_id(object): id of the tenant_id
            key(object): key value user stored in the database.
            data(object): value mapped for key.
            ttl(object): Time to Live for the keyvalue pair in the database.
        """
        try:
            if not self.RecordExists(object.tenant_id, object.key):
                storage = self.TenantStorage(object.tenant_id)
                if storage + len(object.data) <= storage_limit:
                    sql = f"INSERT INTO {self.table_name} (tenant_id, key, data, size, expiry_time) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP + INTERVAL '%s days')"
                    self.cursor.execute(sql, (object.tenant_id, object.key, object.data, len(object.data), object.ttl))
                    self.database.commit()
                    return True
                return f"Storage limit exceeded. Maximum Storage: {storage_limit}, UsedStorage: {storage}, Available: {storage_limit-storage}, dataSize: {len(object.data)} "
            return f"Record {object} already exists in the database"
        except OperationalError as e:
            print(f"Error connecting to database: {e}")
            raise Exception(e)
        except Error as e:
            print(f"Error inserting data: {e}")
            raise Exception(e)


    def disconnect(self):
        try:
            if self.database:
                self.database.disconnect()
                print("Connection to PostgreSQL database disconnected successfully.")
        except Exception as err:
            print("Error while disconnecting the PostgreSQL database connection.")
            raise Exception(err)
