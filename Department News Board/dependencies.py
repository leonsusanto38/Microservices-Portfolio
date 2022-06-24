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

    def get_all_news(self):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []

        sql = "SELECT * FROM news WHERE upload_date >= DATE_SUB(curdate(), INTERVAL 30 DAY)"
        cursor.execute(sql)

        if (cursor.rowcount > 0):
            for row in cursor.fetchall():
                result.append({
                    'id': row['id'],
                    'writer': row['writer'],
                    'news': row['news'],
                    'upload_date': row['upload_date']
                }) 
                
            cursor.close()
            return result
        else:
            return None

    def get_news_by_id(self, news_id):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []

        sql = "SELECT * FROM news WHERE id = '{}' AND upload_date >= DATE_SUB(curdate(), INTERVAL 30 DAY)".format(news_id)
        cursor.execute(sql)

        if (cursor.rowcount > 0):
            result = cursor.fetchone()
            cursor.close()
            return result
        else:
            return None

    def add_news(self, writer, news):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []

        sql = "INSERT INTO news VALUES (0, '{}', '{}', CURRENT_DATE)".format(writer, news)
        cursor.execute(sql)
        self.connection.commit()

        sql = "SELECT * FROM news ORDER BY id DESC LIMIT 1"
        cursor.execute(sql)
        
        if (cursor.rowcount > 0):
            result = cursor.fetchone()
            cursor.close()
            return result
        else:
            return False

    def edit_news(self, news_id, writer, news):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        
        sql = "UPDATE news SET writer = '{}', news = '{}', upload_date = CURRENT_DATE WHERE id = '{}'".format(writer, news, news_id)
        cursor.execute(sql)
        self.connection.commit()
        
        sql = "SELECT * FROM news WHERE id = '{}'".format(news_id)
        cursor.execute(sql)

        if (cursor.rowcount > 0):
            result = cursor.fetchone()
            cursor.close()
            return result
        else:
            return None

    def delete_news(self, news_id):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []

        sql = "SELECT * FROM news WHERE id = '{}'".format(news_id)
        cursor.execute(sql)
        result = cursor.fetchone()
        
        if (cursor.rowcount > 0):
            sql = "DELETE FROM news WHERE id = '{}'".format(news_id)
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            return result
        else: 
            cursor.close()
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
                database='department_news_board',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())