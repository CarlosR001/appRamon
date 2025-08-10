import tkinter as tk
from tkinter import ttk
from datetime import datetime

class DailyDetailView(tk.Toplevel):
    def __init__(self, parent, sales_data, sale_date):
        super().__init__(parent)
        self.sales_data = sales_data
        
        # --- Window Setup ---
        formatted_date = sale_date.strftime('%d/%m/%Y') if isinstance(sale_date, datetime.date) else sale_date
        self.title(f"Detalle de Ventas - {formatted_date}")
        self.geometry("700x400")
        self.grab_set()

        # --- Layout Principal (2 columnas) ---
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(expand=True, fill="both")
        main_frame.columnconfigure(1, weight=1) # El panel derecho se expande
        main_frame.rowconfigure(0, weight=1)

        # --- Panel Izquierdo: Lista de Ventas ---
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        left_frame.rowconfigure(1, weight=1)

        ttk.Label(left_frame, text="Ventas del Día", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w")

        self.sales_tree = ttk.Treeview(left_frame, columns=("id", "hora", "total"), show="headings", height=10)
        self.sales_tree.heading("id", text="ID")
        self.sales_tree.heading("hora", text="Hora")
        self.sales_tree.heading("total", text="Total")
        self.sales_tree.column("id", width=50, anchor="c")
        self.sales_tree.column("hora", width=80, anchor="c")
        self.sales_tree.column("total", width=90, anchor="e")
        self.sales_tree.grid(row=1, column=0, sticky="ns")
        self.sales_tree.bind("<<TreeviewSelect>>", self.on_sale_selected)

        # --- Panel Derecho: Detalle de la Venta Seleccionada ---
        right_frame = ttk.Frame(main_frame, style="Card.TFrame", padding=15)
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.rowconfigure(2, weight=1)
        right_frame.columnconfigure(0, weight=1)

        self.detail_title_var = tk.StringVar(value="Detalle de Venta")
        ttk.Label(right_frame, textvariable=self.detail_title_var, font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w")
        
        self.client_var = tk.StringVar()
        ttk.Label(right_frame, textvariable=self.client_var).grid(row=1, column=0, sticky="w", pady=(0,10))

        self.items_tree = ttk.Treeview(right_frame, columns=("qty", "prod", "price", "subtotal"), show="headings")
        self.items_tree.heading("qty", text="Cant.")
        self.items_tree.heading("prod", text="Producto")
        self.items_tree.heading("price", text="P. Unit.")
        self.items_tree.heading("subtotal", text="Subtotal")
        self.items_tree.column("qty", width=40, anchor="c")
        self.items_tree.column("prod", width=200, anchor="w")
        self.items_tree.column("price", width=80, anchor="e")
        self.items_tree.column("subtotal", width=80, anchor="e")
        self.items_tree.grid(row=2, column=0, sticky="nsew")

        # Rellenar la lista de ventas inicial
        self.populate_sales_list()

    def populate_sales_list(self):
        """Llena la tabla de la izquierda con las ventas del día."""
        for sale in self.sales_data:
            hora = sale['fecha'].strftime('%H:%M:%S') if isinstance(sale['fecha'], datetime) else ''
            total = f"S/ {sale['total']:.2f}"
            self.sales_tree.insert("", "end", iid=sale['id'], values=(sale['id'], hora, total))

    def on_sale_selected(self, event):
        """Se activa al seleccionar una venta, muestra sus detalles a la derecha."""
        selection = self.sales_tree.selection()
        if not selection: return

        sale_id = int(selection[0])
        
        # Encontrar los datos de esta venta en la lista
        selected_sale_data = next((s for s in self.sales_data if s['id'] == sale_id), None)
        
        if selected_sale_data:
            self.detail_title_var.set(f"Detalle de Venta #{sale_id}")
            self.client_var.set(f"Cliente: {selected_sale_data.get('cliente_nombre', 'Público General')}")

            # Limpiar y rellenar la tabla de items
            self.items_tree.delete(*self.items_tree.get_children())
            for item in selected_sale_data.get('items', []):
                price = item['precio_unitario']
                qty = item['cantidad']
                subtotal = f"S/ {price * qty:.2f}"
                price_f = f"S/ {price:.2f}"
                self.items_tree.insert("", "end", values=(qty, item['producto_nombre'], price_f, subtotal))
