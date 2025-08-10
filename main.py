import tkinter as tk
from tkinter import ttk, messagebox
from database import get_db_connection
from auth import verify_password

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Iniciar Sesión")
        self.geometry("300x150")
        self.resizable(False, False)

        # UI Elements
        self.username_label = ttk.Label(self, text="Usuario:")
        self.username_label.pack(pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack(pady=5)

        self.password_label = ttk.Label(self, text="Contraseña:")
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ttk.Button(self, text="Ingresar", command=self.attempt_login)
        self.login_button.pack(pady=10)
        
        # Centrar la ventana
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')


    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Usuario y contraseña son requeridos.")
            return

        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Error de Conexión", "No se pudo conectar a la base de datos.")
            return
            
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT password_hash, id_rol FROM usuarios WHERE nombre_usuario = %s", (username,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if user_data and verify_password(user_data['password_hash'], password):
            messagebox.showinfo("Éxito", "Inicio de sesión correcto.")
            self.destroy() # Cierra la ventana de login
            # Aquí llamaremos a la ventana principal de la aplicación
            main_app = App(user_data['id_rol'])
            main_app.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


class App(tk.Tk):
    def __init__(self, user_role):
        super().__init__()
        self.user_role = user_role
        self.title("Sistema de Ventas e Inventario")
        self.geometry("1024x768")
        
        self.create_widgets()

    def create_widgets(self):
        # Aquí construiremos la interfaz principal, 
        # mostrando/ocultando botones según self.user_role
        
        # Por ahora, solo mostramos el rol
        role_map = {1: "Administrador", 2: "Vendedor", 3: "Tecnico"}
        label = ttk.Label(self, text=f"Bienvenido. Rol: {role_map.get(self.user_role, 'Desconocido')}", font=("Arial", 16))
        label.pack(pady=20)


if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()
