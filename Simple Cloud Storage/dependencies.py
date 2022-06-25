import os
from nameko.extensions import DependencyProvider
import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

class DatabaseWrapper:
    connection = None

    def __init__(self, connection):
        self.connection = connection

    def register(self, username, password):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []

        sql = "SELECT * FROM user WHERE username = '{}'".format(username)
        cursor.execute(sql)
        
        if (cursor.rowcount > 0):
            cursor.close()
            return None
        else:
            sql = "INSERT INTO user VALUES('{}', '{}')".format(username, password)
            cursor.execute(sql)
            self.connection.commit()

            sql = "SELECT * FROM user WHERE username = '{}' AND password = '{}'".format(username, password)
            cursor.execute(sql)
            result = cursor.fetchone()
            cursor.close()
            return result 

    def login(self, username, password):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = "SELECT * FROM user WHERE username = '{}' AND password = '{}'".format(username, password)
        cursor.execute(sql)

        if (cursor.rowcount > 0):
            result = cursor.fetchone()
            cursor.close()
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
                database='simple_cloud_storage',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())