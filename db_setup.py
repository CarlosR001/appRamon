import os
import sqlite3
from tkinter import messagebox

DB_FILE = "tienda_electronica.db"
SQL_FILE = "setup_database.sql"

def execute_sql_from_file(conn, filename):
    """Ejecuta un script SQL completo en la conexión de la base de datos."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al ejecutar el script SQL: {e}")
        messagebox.showerror("Error Crítico de Base de Datos", f"No se pudo ejecutar el script de configuración '{filename}': {e}")
        return False
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo SQL '{filename}'.")
        messagebox.showerror("Error Crítico de Archivo", f"No se encontró el archivo de configuración '{filename}'. La aplicación no puede iniciarse.")
        return False

def setup_database_if_needed():
    """
    Comprueba si la base de datos existe. Si no, la crea y la puebla.
    Devuelve True si la base de datos está lista para usar, False si no.
    """
    if not os.path.exists(DB_FILE):
        print("Base de datos no encontrada. Creando y configurando...")
        try:
            conn = sqlite3.connect(DB_FILE)
            if execute_sql_from_file(conn, SQL_FILE):
                print("Base de datos creada y configurada con éxito.")
                messagebox.showinfo("Configuración Inicial Completa", "La base de datos ha sido configurada por primera vez. La aplicación se iniciará ahora.")
                conn.close()
                return True
            else:
                # Si el script falla, borrar el archivo .db corrupto
                conn.close()
                os.remove(DB_FILE)
                return False
        except sqlite3.Error as e:
            print(f"Error al crear la base de datos: {e}")
            messagebox.showerror("Error Crítico de Base de Datos", f"No se pudo crear el archivo de base de datos: {e}")
            return False
    return True # La base de datos ya existe y está lista
