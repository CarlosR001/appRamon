import tkinter as tk
from tkinter import ttk

class NavigationView(ttk.Frame):
    def __init__(self, parent, app_controller, permissions, logout_command):
        super().__init__(parent, style="Card.TFrame", padding=10)
        self.app_controller = app_controller
        self.permissions = permissions
        self.logout_command = logout_command
        self.buttons = {}
        self.columnconfigure(0, weight=1)

        app_title = ttk.Label(self, text="Centro electronico Ramon", font=("Segoe UI", 18, "bold"))
        app_title.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        self.create_buttons()

    def create_buttons(self):
        all_buttons = [
            ('access_dashboard', "🏠  Dashboard", self.app_controller.show_dashboard_view),
            ('access_sales', "🛒  Ventas (TPV)", self.app_controller.show_sales_view),
            ('access_purchases', "📥  Compras", self.app_controller.show_purchases_view),
            ('access_inventory', "≡  Inventario", self.app_controller.show_inventory_view),
            ('access_clients', "👥  Clientes", self.app_controller.show_clients_view),
            ('access_services', "🔧  Servicios", self.app_controller.show_services_view),
            ('access_sales_history', "🧾  Historial de Ventas", self.app_controller.show_sales_history_view),
            ('access_suppliers', "🚚  Proveedores", self.app_controller.show_suppliers_view),
            ('access_expenses', "💸  Gastos", self.app_controller.show_expenses_view),
            ('access_reports', "📊  Reportes", self.app_controller.show_reports_view),
        ]

        row_index = 1
        for permission, text, command in all_buttons:
            if permission in self.permissions:
                button = ttk.Button(self, text=text, command=command)
                button.grid(row=row_index, column=0, sticky="ew", pady=2)
                self.buttons[permission] = button
                row_index += 1
        
        if 'access_dashboard' in self.buttons:
            self.buttons['access_dashboard'].config(style="Accent.TButton")

        self.grid_rowconfigure(row_index, weight=1)
        row_index += 1

        if 'access_users' in self.permissions:
            self.settings_button = ttk.Button(self, text="⚙️  Gestión de Usuarios", command=self.app_controller.show_users_view)
            self.settings_button.grid(row=row_index, column=0, sticky="ew", pady=(2,10))
            row_index += 1

        self.logout_button = ttk.Button(self, text="↩️  Cerrar Sesión", command=self.logout_command)
        self.logout_button.grid(row=row_index, column=0, sticky="ew", pady=(5,0))
