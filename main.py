# Punto de entrada principal de la aplicación
import tkinter as tk
from tkinter import ttk, messagebox

from database import get_db_connection
from auth import verify_password
from views.products_view import ProductsView
from views.navigation_view import NavigationView
import product_model as p_model
from product_controller import ProductController

class LoginWindow(tk.Tk):
    # --- El código de LoginWindow no cambia ---
    def __init__(self):
        super().__init__()
        self.title("Iniciar Sesión")
        self.geometry("300x150")
        self.resizable(False, False)
        self.create_widgets()
        self.center_window()

    def create_widgets(self):
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
        self.title("Electro-Pro: Sistema de Gestión")
        self.geometry("1280x720")
        self.minsize(1000, 600) # Establecer un tamaño mínimo

        # Configurar el layout principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1) # El área de contenido se expandirá

        # Crear las vistas principales
        self.views = {}
        self.create_views()

        # Inicializar los controladores
        self.initialize_controllers()
        
        # Mostrar la vista de inventario por defecto
        self.show_inventory_view()

    def create_views(self):
        """Crea el layout principal con navegación y área de contenido."""
        # Panel de Navegación
        self.navigation_view = NavigationView(self, self)
        self.navigation_view.grid(row=0, column=0, sticky="nsw")

        # Área de Contenido (un Frame que contendrá las vistas de cada módulo)
        self.main_content_frame = ttk.Frame(self)
        self.main_content_frame.grid(row=0, column=1, sticky="nsew")
        self.main_content_frame.grid_rowconfigure(0, weight=1)
        self.main_content_frame.grid_columnconfigure(0, weight=1)

        # Crear la vista de productos pero no mostrarla todavía
        self.products_view = ProductsView(self.main_content_frame, self.user_role)
        self.views['inventory'] = self.products_view
        # Aquí se crearían las otras vistas (ventas, servicios, etc.)

    def show_view(self, view_name):
        """Muestra una vista en el área de contenido principal."""
        for view in self.views.values():
            view.grid_remove() # Oculta todas las vistas
        
        view_to_show = self.views.get(view_name)
        if view_to_show:
            view_to_show.grid(row=0, column=0, sticky="nsew") # Muestra la vista deseada

    def show_inventory_view(self):
        """Muestra específicamente la vista de inventario."""
        self.show_view('inventory')
        self.load_products_data() # Carga los datos cada vez que se muestra

    def initialize_controllers(self):
        self.controller = ProductController(self)

    def load_products_data(self):
        """Carga los productos y los muestra en la tabla."""
        if 'inventory' in self.views:
            self.products_view.clear_tree()
            products_list = p_model.get_all_products()
            for product in products_list:
                self.products_view.add_product_to_tree(product)


if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()
