# Punto de entrada principal de la aplicación
import tkinter as tk
from tkinter import ttk, messagebox

from database import get_db_connection
from auth import verify_password
from views.products_view import ProductsView
import product_model as p_model
from product_controller import ProductController

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Iniciar Sesión")
        self.geometry("300x150")
        self.resizable(False, False)
        self.create_widgets()
        self.center_window()

    def create_widgets(self):
        # ... (código sin cambios)
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

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # ... (código sin cambios)
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
            self.destroy()
            main_app = App(user_data['id_rol'])
            main_app.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


class App(tk.Tk):
    def __init__(self, user_role):
        super().__init__()
        self.user_role = user_role
        self.title("Sistema de Ventas e Inventario")
        self.geometry("1200x700")
        
        self.create_widgets()
        # Inicializar el controlador
        self.initialize_controllers()
        
        # Cargar datos iniciales
        self.load_products_data()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        self.products_view = ProductsView(self.notebook, self.user_role)
        self.notebook.add(self.products_view, text="Inventario")
        # Aquí se añadirán más pestañas en el futuro

    def initialize_controllers(self):
        """Crea las instancias de los controladores."""
        # 'self' (la instancia de App) se pasa al controlador para que pueda acceder a sus métodos y atributos.
        self.controller = ProductController(self)

    def load_products_data(self):
        """Carga los productos de la BD y los muestra en la tabla."""
        self.products_view.clear_tree()
        products_list = p_model.get_all_products()
        for product in products_list:
            # El formato del precio se delega a la vista
            self.products_view.add_product_to_tree(product)


if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()
