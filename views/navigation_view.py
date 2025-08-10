import tkinter as tk
from tkinter import ttk

class NavigationView(ttk.Frame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, style="Card.TFrame", padding=10)
        self.app_controller = app_controller # Renombramos para mayor claridad

        self.columnconfigure(0, weight=1)

        app_title = ttk.Label(self, text="ELECTRO-PRO", font=("Segoe UI", 18, "bold"))
        app_title.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        # --- Botones de Navegación ---
        # El controlador principal (App) se encarga de mostrar las vistas
        self.sales_button = ttk.Button(self, text="🛒  Ventas (TPV)", command=self.app_controller.show_sales_view, style="Accent.TButton")
        self.sales_button.grid(row=1, column=0, sticky="ew", pady=2)
        
        self.inventory_button = ttk.Button(self, text="≡  Inventario", command=self.app_controller.show_inventory_view)
        self.inventory_button.grid(row=2, column=0, sticky="ew", pady=2)

        self.services_button = ttk.Button(self, text="🔧  Servicios", state="disabled")
        self.services_button.grid(row=3, column=0, sticky="ew", pady=2)

        self.reports_button = ttk.Button(self, text="📊  Reportes", state="disabled")
        self.reports_button.grid(row=4, column=0, sticky="ew", pady=2)

        self.grid_rowconfigure(5, weight=1) 

        self.settings_button = ttk.Button(self, text="⚙️  Configuración", state="disabled")
        self.settings_button.grid(row=6, column=0, sticky="ew", pady=10)
