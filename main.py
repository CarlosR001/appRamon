# Punto de entrada principal de la aplicación
import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk # Importamos la librería de temas

from database import get_db_connection
from auth import verify_password
from views.products_view import ProductsView
from views.navigation_view import NavigationView
import product_model as p_model
from product_controller import ProductController

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        sv_ttk.set_theme("dark") # Aplicar tema oscuro a la ventana de login
        self.title("Iniciar Sesión")
        self.geometry("300x180") # Aumentamos la altura para que quepa el botón
        self.resizable(False, False)
        self.create_widgets()
        self.center_window()

    def create_widgets(self):
        # El tema se encarga del estilo, ya no necesitamos frames extras
        self.username_label = ttk.Label(self, text="Usuario:")
        self.username_label.pack(pady=(10, 0))
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack(pady=5, padx=20, fill="x")
        self.password_label = ttk.Label(self, text="Contraseña:")
        self.password_label.pack(pady=(10, 0))
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(pady=5, padx=20, fill="x")
        self.login_button = ttk.Button(self, text="Ingresar", command=self.attempt_login, style="Accent.TButton")
        self.login_button.pack(pady=10)

    def center_window(self):
        # ... (código sin cambios)
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def attempt_login(self):
        # ... (código sin cambios)
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
        
        # Aplicar el tema ANTES de crear cualquier widget
        sv_ttk.set_theme("dark")

        self.title("Electro-Pro: Sistema de Gestión")
        self.geometry("1280x720")
        self.minsize(1000, 600)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.views = {}
        self.create_views()
        self.initialize_controllers()
        self.show_inventory_view()

    def create_views(self):
        # Quitamos el estilo manual de NavigationView, el tema lo manejará
        self.navigation_view = NavigationView(self, self)
        self.navigation_view.grid(row=0, column=0, sticky="nsw")

        self.main_content_frame = ttk.Frame(self)
        self.main_content_frame.grid(row=0, column=1, sticky="nsew")
        self.main_content_frame.grid_rowconfigure(0, weight=1)
        self.main_content_frame.grid_columnconfigure(0, weight=1)

        self.products_view = ProductsView(self.main_content_frame, self.user_role)
        self.views['inventory'] = self.products_view

    def show_view(self, view_name):
        # ... (código sin cambios)
        for view in self.views.values():
            view.grid_remove()
        view_to_show = self.views.get(view_name)
        if view_to_show:
            view_to_show.grid(row=0, column=0, sticky="nsew")

    def show_inventory_view(self):
        # ... (código sin cambios)
        self.show_view('inventory')
        self.load_products_data()

    def initialize_controllers(self):
        self.controller = ProductController(self)

    def load_products_data(self):
        # ... (código sin cambios)
        if 'inventory' in self.views:
            self.products_view.clear_tree()
            products_list = p_model.get_all_products()
            for product in products_list:
                self.products_view.add_product_to_tree(product)


if __name__ == "__main__":
    # La aplicación principal (Login) ya inicializa el tema
    login_window = LoginWindow()
    login_window.mainloop()
