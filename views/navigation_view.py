import tkinter as tk
from tkinter import ttk

class NavigationView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Nav.TFrame")
        self.controller = controller

        # Estilo para el Frame de navegación
        style = ttk.Style()
        style.configure("Nav.TFrame", background="#2c3e50") # Un color oscuro y moderno
        style.configure("Nav.TButton", 
                        font=("Arial", 12, "bold"), 
                        background="#2c3e50",
                        foreground="white",
                        padding=(10, 15))
        style.map("Nav.TButton", 
                  background=[("active", "#34495e")], # Color al pasar el ratón
                  foreground=[("active", "white")])

        self.columnconfigure(0, weight=1)

        # Título de la App
        app_title = ttk.Label(self, text="ELECTRO-PRO", font=("Arial", 20, "bold"), background="#2c3e50", foreground="white", padding=(10, 20))
        app_title.grid(row=0, column=0, sticky="ew", pady=(10, 20))

        # --- Botones de Navegación ---
        self.inventory_button = ttk.Button(self, text="≡  Inventario", style="Nav.TButton", command=self.controller.show_inventory_view)
        self.inventory_button.grid(row=1, column=0, sticky="ew", padx=10, pady=2)

        self.sales_button = ttk.Button(self, text="🛒  Ventas (TPV)", style="Nav.TButton", state="disabled") # Deshabilitado por ahora
        self.sales_button.grid(row=2, column=0, sticky="ew", padx=10, pady=2)

        self.services_button = ttk.Button(self, text="🔧  Servicios", style="Nav.TButton", state="disabled")
        self.services_button.grid(row=3, column=0, sticky="ew", padx=10, pady=2)

        self.reports_button = ttk.Button(self, text="📊  Reportes", style="Nav.TButton", state="disabled")
        self.reports_button.grid(row=4, column=0, sticky="ew", padx=10, pady=2)

        # Espaciador para empujar el botón de configuración hacia abajo
        self.grid_rowconfigure(5, weight=1) 

        self.settings_button = ttk.Button(self, text="⚙️  Configuración", style="Nav.TButton", state="disabled")
        self.settings_button.grid(row=6, column=0, sticky="ew", padx=10, pady=(10,20))

