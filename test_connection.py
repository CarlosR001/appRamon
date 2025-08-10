import configparser
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
import tkinter as tk

def test_db_connection():
    """
    Intenta conectarse a la base de datos MySQL usando config.ini.
    Muestra un messagebox con el resultado.
    """
    # Ocultar la ventana raíz de tkinter
    root = tk.Tk()
    root.withdraw()

    # Leer config.ini
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        db_config = config['database']
    except Exception as e:
        messagebox.showerror("Error de Configuración", f"No se pudo leer el archivo 'config.ini'.\n\nAsegúrese de que el archivo existe y está en la misma carpeta que el ejecutable.\n\nError: {e}")
        return

    # Intentar conectar
    try:
        print("Intentando conectar con la siguiente configuración:")
        print(f"Host: {db_config.get('host')}")
        print(f"User: {db_config.get('user')}")
        print(f"Database: {db_config.get('database')}")
        
        conn = mysql.connector.connect(
            host=db_config.get('host'),
            user=db_config.get('user'),
            password=db_config.get('password', ''),
            database=db_config.get('database')
        )
        if conn.is_connected():
            conn.close()
            messagebox.showinfo("¡Éxito!", "La conexión a la base de datos MySQL se ha realizado correctamente.")
            
    except Error as e:
        messagebox.showerror("¡Fallo en la Conexión!", f"No se pudo conectar a la base de datos MySQL.\n\n"
                                                      f"Error de MySQL: {e}\n\n"
                                                      "Posibles causas:\n"
                                                      "1. El servicio de MySQL (XAMPP) no está iniciado.\n"
                                                      "2. El nombre de la base de datos, el usuario o la contraseña en 'config.ini' son incorrectos.\n"
                                                      "3. El Firewall de Windows está bloqueando la conexión.")

if __name__ == "__main__":
    test_db_connection()
