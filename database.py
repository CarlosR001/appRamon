import sqlite3
from sqlite3 import Error

DB_FILE = "tienda_electronica.db"

def get_db_connection():
    """
    Crea una conexión a la base de datos SQLite.
    La conexión devolverá filas que se pueden acceder por nombre de columna.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        # Este modo permite acceder a las columnas por nombre (como un diccionario)
        conn.row_factory = sqlite3.Row
    except Error as e:
        print(f"Error al conectar a SQLite: {e}")
        return None
    return conn
