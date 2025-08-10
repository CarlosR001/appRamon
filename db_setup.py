import os
import sys
import sqlite3
from tkinter import messagebox

DB_FILE = "tienda_electronica.db"

def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller. """
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

SQL_FILE = resource_path("setup_database.sql")

def execute_sql_from_file(conn, filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()
        return True
    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"No se pudo ejecutar el script '{filename}': {e}")
        return False
    except FileNotFoundError:
        messagebox.showerror("Error de Archivo", f"No se encontró el archivo de configuración '{filename}'.")
        return False

def setup_database_if_needed():
    if not os.path.exists(DB_FILE):
        print("Base de datos no encontrada. Creando y configurando...")
        try:
            conn = sqlite3.connect(DB_FILE)
            if execute_sql_from_file(conn, SQL_FILE):
                print("Base de datos creada y configurada con éxito.")
                messagebox.showinfo("Configuración Completa", "La base de datos ha sido configurada. La aplicación se iniciará ahora.")
                conn.close()
                return True
            else:
                conn.close()
                if os.path.exists(DB_FILE): os.remove(DB_FILE)
                return False
        except sqlite3.Error as e:
            messagebox.showerror("Error Crítico", f"No se pudo crear la base de datos: {e}")
            return False
    return True
