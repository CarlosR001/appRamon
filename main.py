# Punto de entrada principal de la aplicación
import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk

# Importaciones de la aplicación
from database import get_db_connection
from auth import verify_password

# Vistas
from views.products_view import ProductsView
from views.navigation_view import NavigationView
from views.sales_view import SalesView
from modules.reports.reports_view import ReportsView

# Controladores
from product_controller import ProductController
from sales_controller import SalesController
from modules.reports.reports_controller import ReportsController


class LoginWindow(tk.Tk):
    # --- El código de LoginWindow no cambia, está correcto ---
    def __init__(self):
        super().__init__()
        sv_ttk.set_theme("dark")
        self.title("Iniciar Sesión")
        self.geometry("300x180")
        self.resizable(False, False)
        self.create_widgets()
        self.center_window()

    def create_widgets(self):
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
        
        sv_ttk.set_theme("dark")
        
        self.title("Electro-Pro: Sistema de Gestión")
        self.geometry("1280x720")
        self.minsize(1100, 650)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.views = {}
        self.controllers = {}
        
        self.create_views()
        self.initialize_controllers()
        
        # Iniciar en la vista de ventas por defecto
        self.show_sales_view()

    def create_views(self):
        """Crea el layout principal y todas las vistas de los módulos."""
        self.navigation_view = NavigationView(self, self)
        self.navigation_view.grid(row=0, column=0, sticky="nsw")
        
        self.main_content_frame = ttk.Frame(self)
        self.main_content_frame.grid(row=0, column=1, sticky="nsew")
        self.main_content_frame.grid_rowconfigure(0, weight=1)
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        
        # Crear vistas y guardarlas en el diccionario
        self.views['inventory'] = ProductsView(self.main_content_frame, self.user_role)
        self.views['sales'] = SalesView(self.main_content_frame)
        self.views['reports'] = ReportsView(self.main_content_frame)

    def initialize_controllers(self):
        """Crea todas las instancias de los controladores."""
        self.controllers['products'] = ProductController(self)
        
        sales_controller = SalesController(self)
        sales_controller.set_view(self.views['sales'])
        self.controllers['sales'] = sales_controller

        reports_controller = ReportsController(self)
        reports_controller.set_view(self.views['reports'])
        self.controllers['reports'] = reports_controller

    def show_view(self, view_name):
        """Oculta todas las vistas y muestra solo la seleccionada."""
        for view in self.views.values():
            view.grid_remove()
        
        view_to_show = self.views.get(view_name)
        if view_to_show:
            view_to_show.grid(row=0, column=0, sticky="nsew")

    def show_inventory_view(self):
        """Muestra la vista de inventario y carga sus datos."""
        self.show_view('inventory')
        self.controllers['products'].load_products()

    def show_sales_view(self):
        """Muestra la vista de ventas."""
        self.show_view('sales')
        self.controllers['sales'].search_products_for_sale("")

    def show_reports_view(self):
        """Muestra la vista de reportes y carga sus datos."""
        self.show_view('reports')
        self.controllers['reports'].load_data()


if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()
