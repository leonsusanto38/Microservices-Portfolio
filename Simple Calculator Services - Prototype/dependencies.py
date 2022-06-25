from nameko.extensions import DependencyProvider
import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

class DatabaseWrapper:
    connection = None

    def __init__(self, connection):
        self.connection = connection

    def get_prime(self, nrp, name, email, password):
        result = []
        
        if (cursor.rowcount > 0):
            return None
        else:
            
            return result 

    def get_prime_palindrome(self, email, password):
        result = []

        if (cursor.rowcount > 0):
            
            return result
        else:
            return None

    def __del__(self):
        self.connection.close()

class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='127.0.0.1',
                database='research_paper_storage_service',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())