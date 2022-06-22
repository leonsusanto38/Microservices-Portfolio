from sqlite3 import Cursor
from unittest import result
from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
import itertools

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def regis(self, a, b):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = "SELECT * from user where username = '{}'".format(a)
        cursor.execute(sql)
        if(cursor.rowcount > 0):
            cursor.close()
            result.append("Username telah terdaftar")
            return result
        else:
            sql = "INSERT INTO user VALUES('{}', '{}')".format(a, b)
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            result.append("Registrasi berhasil")
            return result
        
    def login(self, a, b):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = "SELECT * from user where username = '{}'".format(a)
        cursor.execute(sql)
        if(cursor.rowcount == 0):
            cursor.close()
            result.append("Username tidak terdaftar")
            return 0
        else:
            resultfetch = cursor.fetchone()
            if(resultfetch['password'] == b):
                cursor.close()
                result.append("Login Berhasil")
                return 1
            else:
                cursor.close()
                result.append("Password salah")
                return 0

    def get_all_news(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM news WHERE upload_date >= DATE_SUB(curdate(), INTERVAL 30 DAY)"
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'username': row['username'],
                'news': row['news'],
                'upload_date': row['upload_date']
            })
        cursor.close()
        return result
    
    def get_news(self, news):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM news WHERE id = {} AND upload_date >= DATE_SUB(curdate(), INTERVAL 30 DAY)".format(news)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def post_news(self, username, news):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = "INSERT INTO news VALUES(0, '{}', '{}', CURRENT_DATE)".format(username, news)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        result.append("News Posted")
        return result
    
    def edit_news(self, id, username, news):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = "UPDATE news SET username = %s, news = %s, upload_date = CURRENT_DATE WHERE id = %s"
        val  = (username, news, id)
        cursor.execute(sql, val)
        self.connection.commit()
        cursor.close()
        result.append("News Edited")
        return result
    
    def delete_news(self, id):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = "DELETE FROM news WHERE id = {}".format(id)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        result.append("News Deleted")
        return result
    
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
                host='localhost',
                database='department_news_board',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
