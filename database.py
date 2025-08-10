import mysql.connector
from mysql.connector import Error
import configparser
import os
import sys

def get_config_path():
    """
    Determina la ruta correcta para config.ini, ya sea en desarrollo o empaquetado.
    """
    if getattr(sys, 'frozen', False):
        # Si la aplicación está empaquetada (frozen) por PyInstaller
        application_path = sys._MEIPASS
    else:
        # Si se está ejecutando como un script normal
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(application_path, 'config.ini')

def get_db_connection():
    """
    Crea una conexión a la base de datos MySQL usando los datos de config.ini.
    """
    config = configparser.ConfigParser()
    config_path = get_config_path()

    # Usar un bloque try-except por si config.ini no existe
    try:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"El archivo de configuración no se encontró en: {config_path}")
        
        config.read(config_path)
        db_config = config['database']
    except Exception as e:
        print(f"Error al leer el archivo de configuración: {e}")
        # En un entorno empaquetado, puede ser útil mostrar este error en un cuadro de diálogo
        # import tkinter as tk
        # from tkinter import messagebox
        # root = tk.Tk()
        # root.withdraw()
        # messagebox.showerror("Error de Configuración", f"No se pudo leer config.ini: {e}")
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
        # import tkinter as tk
        # from tkinter import messagebox
        # root = tk.Tk()
        # root.withdraw()
        # messagebox.showerror("Error de Base de Datos", f"No se pudo conectar a MySQL: {e}")
        return None
    return None
