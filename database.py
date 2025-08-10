import mysql.connector
from mysql.connector import Error
import configparser

def get_db_connection():
    """
    Crea una conexión a la base de datos MySQL usando los datos de config.ini.
    """
    config = configparser.ConfigParser()
    # Usar un bloque try-except por si config.ini no existe
    try:
        config.read('config.ini')
        db_config = config['database']
    except Exception as e:
        print(f"Error al leer config.ini: {e}")
        return None

    try:
        conn = mysql.connector.connect(
            host=db_config.get('host', 'localhost'),
            user=db_config.get('user', 'root'),
            password=db_config.get('password', ''),
            database=db_config.get('database', 'tienda_electronica')
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None
    return None
