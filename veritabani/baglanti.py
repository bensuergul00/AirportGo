import mysql.connector
from mysql.connector import Error

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "airport_go_db"
DB_PORT = 8889            #

def baglanti_al():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        if conn.is_connected():
            return conn
        return None
    except Error as e:
        print("Veritabanına bağlanılamadı:", e)
        return None
