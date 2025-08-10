import tkinter as tk
from tkinter import ttk

class NavigationView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Card.TFrame", padding=10) # Usamos el estilo 'Card' del tema
        self.controller = controller

        self.columnconfigure(0, weight=1)

        # Título de la App
        # Usamos los estilos del tema, ya no definimos colores manualmente
        app_title = ttk.Label(self, text="ELECTRO-PRO", font=("Segoe UI", 18, "bold"))
        app_title.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        # --- Botones de Navegación ---
        # El estilo de los botones es manejado por el tema sv-ttk
        # El estilo 'Accent.TButton' le da un color especial al botón principal
        self.inventory_button = ttk.Button(self, text="≡  Inventario", command=self.controller.show_inventory_view, style="Accent.TButton")
        self.inventory_button.grid(row=1, column=0, sticky="ew", pady=2)

        self.sales_button = ttk.Button(self, text="🛒  Ventas (TPV)", state="disabled")
        self.sales_button.grid(row=2, column=0, sticky="ew", pady=2)

        self.services_button = ttk.Button(self, text="🔧  Servicios", state="disabled")
        self.services_button.grid(row=3, column=0, sticky="ew", pady=2)

        self.reports_button = ttk.Button(self, text="📊  Reportes", state="disabled")
        self.reports_button.grid(row=4, column=0, sticky="ew", pady=2)

        # Espaciador para empujar el botón de configuración hacia abajo
        self.grid_rowconfigure(5, weight=1) 

        self.settings_button = ttk.Button(self, text="⚙️  Configuración", state="disabled")
        self.settings_button.grid(row=6, column=0, sticky="ew", pady=10)
