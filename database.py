import mysql.connector
from mysql.connector import Error
import configparser

def get_db_connection():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    try:
        conn = mysql.connector.connect(
            host=config['database']['host'],
            user=config['database']['user'],
            password=config['database']['password'],
            database=config['database']['database']
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None
