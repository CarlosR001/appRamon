import tkinter as tk
from tkinter import ttk

class NavigationView(ttk.Frame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, style="Card.TFrame", padding=10)
        self.app_controller = app_controller

        self.columnconfigure(0, weight=1)

        # --- NOMBRE DE LA TIENDA (AQUÍ PUEDES CAMBIARLO) ---
        app_title = ttk.Label(self, text="Electronica Ramon Planta", font=("Segoe UI", 18, "bold"))
        app_title.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        # --- Botones de Flujo Principal ---
        self.sales_button = ttk.Button(self, text="🛒  Ventas (TPV)", command=self.app_controller.show_sales_view, style="Accent.TButton")
        self.sales_button.grid(row=1, column=0, sticky="ew", pady=2)

        self.purchases_button = ttk.Button(self, text="📥  Compras", command=self.app_controller.show_purchases_view)
        self.purchases_button.grid(row=2, column=0, sticky="ew", pady=2)

        self.inventory_button = ttk.Button(self, text="≡  Inventario", command=self.app_controller.show_inventory_view)
        self.inventory_button.grid(row=3, column=0, sticky="ew", pady=2)

        self.clients_button = ttk.Button(self, text="👥  Clientes", command=self.app_controller.show_clients_view)
        self.clients_button.grid(row=4, column=0, sticky="ew", pady=2)

        self.services_button = ttk.Button(self, text="🔧  Servicios", command=self.app_controller.show_services_view)
        self.services_button.grid(row=5, column=0, sticky="ew", pady=2)

        # --- Botones solo para Administradores ---
        is_admin = (self.app_controller.user_role == 1)
        admin_state = tk.NORMAL if is_admin else tk.DISABLED

        self.suppliers_button = ttk.Button(self, text="🚚  Proveedores", command=self.app_controller.show_suppliers_view, state=admin_state)
        self.suppliers_button.grid(row=6, column=0, sticky="ew", pady=2)

        self.expenses_button = ttk.Button(self, text="💸  Gastos", command=self.app_controller.show_expenses_view, state=admin_state)
        self.expenses_button.grid(row=7, column=0, sticky="ew", pady=2)

        self.reports_button = ttk.Button(self, text="📊  Reportes", command=self.app_controller.show_reports_view, state=admin_state)
        self.reports_button.grid(row=8, column=0, sticky="ew", pady=2)

        self.grid_rowconfigure(9, weight=1) 

        self.settings_button = ttk.Button(self, text="⚙️  Gestión de Usuarios", command=self.app_controller.show_users_view, state=admin_state)
        self.settings_button.grid(row=10, column=0, sticky="ew", pady=10)
