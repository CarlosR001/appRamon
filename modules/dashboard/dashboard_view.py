import tkinter as tk
from tkinter import ttk

class DashboardView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self.controller = None

        # --- Layout Principal ---
        self.columnconfigure((0, 1, 2), weight=1)
        self.rowconfigure(0, weight=1)

        # --- Creación de las tarjetas ---
        self.create_info_card(0, "Ventas de Hoy", "S/ 0.00", "#77dd77")
        self.create_info_card(1, "Servicios Pendientes", "0", "#fdfd96")
        self.create_info_card(2, "Productos con Bajo Stock", "0", "#ff6961")

    def set_controller(self, controller):
        self.controller = controller

    def create_info_card(self, column, title, initial_value, color):
        """Crea una tarjeta de información estilizada."""
        card = ttk.LabelFrame(self, text=title, padding=(20, 10))
        card.grid(row=0, column=column, sticky="nsew", padx=10, pady=10)
        card.columnconfigure(0, weight=1)

        # Usamos un Label para el valor grande
        value_var = tk.StringVar(value=initial_value)
        value_label = ttk.Label(card, textvariable=value_var, font=("Segoe UI", 36, "bold"))
        value_label.pack(expand=True)
        
        # Guardamos la variable para poder actualizarla después
        if "Ventas" in title:
            self.today_revenue_var = value_var
        elif "Servicios" in title:
            self.pending_services_var = value_var
        elif "Stock" in title:
            self.low_stock_items_var = value_var

    def update_data(self, data):
        """Actualiza los valores de las tarjetas con los nuevos datos."""
        today_revenue = data.get('today_revenue', 0.0)
        pending_services = data.get('pending_services', 0)
        low_stock_items = data.get('low_stock_items', 0)

        self.today_revenue_var.set(f"S/ {today_revenue:.2f}")
        self.pending_services_var.set(str(pending_services))
        self.low_stock_items_var.set(str(low_stock_items))
