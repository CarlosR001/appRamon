# Punto de entrada principal de la aplicación
import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk

# Importaciones de la aplicación
from database import get_db_connection
from auth import verify_and_get_user

# Vistas
from views.products_view import ProductsView
from views.navigation_view import NavigationView
from views.sales_view import SalesView
from modules.reports.reports_view import ReportsView
from modules.clients.client_view import ClientsView
from modules.services.service_view import ServicesView
from modules.expenses.expense_view import ExpensesView
from modules.suppliers.supplier_view import SupplierView
from modules.purchases.purchase_view import PurchaseView
from modules.users.user_view import UserView
from modules.dashboard.dashboard_view import DashboardView
from modules.sales_history.sales_history_view import SalesHistoryView

# Controladores
from product_controller import ProductController
from sales_controller import SalesController
from modules.reports.reports_controller import ReportsController
from modules.clients.client_controller import ClientController
from modules.services.service_controller import ServiceController
from modules.expenses.expense_controller import ExpenseController
from modules.suppliers.supplier_controller import SupplierController
from modules.purchases.purchase_controller import PurchaseController
from modules.users.user_controller import UserController
from modules.dashboard.dashboard_controller import DashboardController
from modules.sales_history.sales_history_controller import SalesHistoryController


class LoginWindow(tk.Tk):
    def __init__(self, on_success_callback):
        super().__init__()
        self.on_success = on_success_callback
        sv_ttk.set_theme("dark")
        self.title("Iniciar Sesión"); self.geometry("300x180"); self.resizable(False, False)
        self.create_widgets(); self.center_window()

    def create_widgets(self):
        self.username_label = ttk.Label(self, text="Usuario:"); self.username_label.pack(pady=(10, 0))
        self.username_entry = ttk.Entry(self); self.username_entry.pack(pady=5, padx=20, fill="x")
        self.password_label = ttk.Label(self, text="Contraseña:"); self.password_label.pack(pady=(10, 0))
        self.password_entry = ttk.Entry(self, show="*"); self.password_entry.pack(pady=5, padx=20, fill="x")
        self.login_button = ttk.Button(self, text="Ingresar", command=self.attempt_login, style="Accent.TButton"); self.login_button.pack(pady=10)

    def center_window(self):
        self.update_idletasks(); width = self.winfo_width(); height = self.winfo_height()
        x = (self.winfo_screenwidth()//2)-(width//2); y = (self.winfo_screenheight()//2)-(height//2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Usuario y contraseña son requeridos."); return
        
        user_data = verify_and_get_user(username, password)
        if user_data:
            self.destroy()
            self.on_success(user_data)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


class App(tk.Tk):
    def __init__(self, user_data, on_logout_callback):
        super().__init__()
        self.user_data = user_data
        self.user_id = user_data.get('id')
        self.user_role = user_data.get('id_rol')
        self.user_permissions = user_data.get('permissions', [])
        self.on_logout = on_logout_callback
        
        sv_ttk.set_theme("dark")
        self.title("Centro electronico Ramon: Sistema de Gestión"); self.geometry("1280x720"); self.minsize(1100, 650)
        self.grid_rowconfigure(0, weight=1); self.grid_columnconfigure(1, weight=1)
        self.views = {}; self.controllers = {}
        self.create_views(); self.initialize_controllers()
        self.show_dashboard_view()

    def create_views(self):
        self.navigation_view = NavigationView(self, self, self.user_permissions, self.logout)
        self.navigation_view.grid(row=0, column=0, sticky="nsw")
        self.main_content_frame = ttk.Frame(self)
        self.main_content_frame.grid(row=0, column=1, sticky="nsew")
        self.main_content_frame.grid_rowconfigure(0, weight=1); self.main_content_frame.grid_columnconfigure(0, weight=1)
        
        self.views['dashboard'] = DashboardView(self.main_content_frame)
        self.views['inventory'] = ProductsView(self.main_content_frame, self.user_role)
        self.views['sales'] = SalesView(self.main_content_frame)
        self.views['reports'] = ReportsView(self.main_content_frame)
        self.views['clients'] = ClientsView(self.main_content_frame)
        self.views['services'] = ServicesView(self.main_content_frame)
        self.views['expenses'] = ExpensesView(self.main_content_frame)
        self.views['suppliers'] = SupplierView(self.main_content_frame)
        self.views['purchases'] = PurchaseView(self.main_content_frame)
        self.views['users'] = UserView(self.main_content_frame)
        self.views['sales_history'] = SalesHistoryView(self.main_content_frame, self.user_role == 1)

    def initialize_controllers(self):
        self.controllers['dashboard'] = DashboardController(self)
        self.controllers['products'] = ProductController(self)
        sales_controller = SalesController(self); sales_controller.set_view(self.views['sales']); self.controllers['sales'] = sales_controller
        reports_controller = ReportsController(self); reports_controller.set_view(self.views['reports']); self.controllers['reports'] = reports_controller
        client_controller = ClientController(self); self.controllers['clients'] = client_controller
        service_controller = ServiceController(self); self.controllers['services'] = service_controller
        expense_controller = ExpenseController(self); self.controllers['expenses'] = expense_controller
        supplier_controller = SupplierController(self); self.controllers['suppliers'] = supplier_controller
        purchase_controller = PurchaseController(self); purchase_controller.set_view(self.views['purchases']); self.controllers['purchases'] = purchase_controller
        user_controller = UserController(self); self.controllers['users'] = user_controller
        self.controllers['sales_history'] = SalesHistoryController(self)

    def show_view(self, view_name):
        for view in self.views.values(): view.grid_remove()
        view_to_show = self.views.get(view_name)
        if view_to_show: view_to_show.grid(row=0, column=0, sticky="nsew")

    def logout(self):
        self.destroy()
        self.on_logout()

    def show_dashboard_view(self):
        self.show_view('dashboard'); self.controllers['dashboard'].load_data()
    def show_inventory_view(self):
        self.show_view('inventory'); self.controllers['products'].load_products()
    def show_sales_view(self):
        self.show_view('sales'); self.controllers['sales'].search_products_for_sale("") 
    def show_reports_view(self):
        self.show_view('reports'); self.controllers['reports'].load_data()
    def show_clients_view(self):
        self.show_view('clients'); self.controllers['clients'].load_all_clients()
    def show_services_view(self):
        self.show_view('services'); self.controllers['services'].load_all_services()
    def show_expenses_view(self):
        self.show_view('expenses'); self.controllers['expenses'].load_all_expenses()
    def show_suppliers_view(self):
        self.show_view('suppliers'); self.controllers['suppliers'].load_all_suppliers()
    def show_purchases_view(self):
        self.show_view('purchases'); self.controllers['purchases'].clear_purchase(confirm=False)
    def show_users_view(self):
        self.show_view('users'); self.controllers['users'].load_initial_data()
    def show_sales_history_view(self):
        self.show_view('sales_history'); self.controllers['sales_history'].load_sales_history()

def start_application():
    """Función que maneja el ciclo de login/logout."""
    def run_main_app(user_data):
        app = App(user_data, on_logout_callback=start_application)
        app.mainloop()

    # Verificar conexión a la BD antes de iniciar
    conn = get_db_connection()
    if conn:
        conn.close()
        login_window = LoginWindow(on_success_callback=run_main_app)
        login_window.mainloop()
    else:
        messagebox.showerror("Error de Conexión Crítico", 
                             "No se pudo conectar a la base de datos MySQL.\n\n"
                             "Por favor, verifique lo siguiente:\n"
                             "1. XAMPP está ejecutándose y el servicio de MySQL está iniciado.\n"
                             "2. Los datos en el archivo 'config.ini' son correctos.\n"
                             "3. La base de datos 'tienda_electronica' ha sido creada.")

if __name__ == "__main__":
    start_application()
