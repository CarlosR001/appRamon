import tkinter as tk
from tkinter import ttk

class SalesView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # --- Layout Principal (2 columnas) ---
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        # --- Columna Izquierda: Búsqueda y Resultados ---
        left_frame = ttk.Frame(self, padding=10)
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
        
        ttk.Label(left_frame, text="Buscar Producto", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(left_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=0, sticky="ew", pady=(0,10), ipady=4)
        search_entry.bind("<KeyRelease>", self.on_key_release)

        # -- Tabla de Búsqueda de Productos (CORREGIDA) --
        self.search_results_tree = ttk.Treeview(left_frame, columns=("nombre", "precio", "stock", "id"), show="headings", displaycolumns=("nombre", "precio", "stock"))
        self.search_results_tree.heading("nombre", text="Producto")
        self.search_results_tree.heading("precio", text="Precio")
        self.search_results_tree.heading("stock", text="Stock")
        self.search_results_tree.column("precio", width=80, anchor=tk.E)
        self.search_results_tree.column("stock", width=60, anchor=tk.CENTER)
        self.search_results_tree.grid(row=1, column=0, sticky="nsew")
        # Esta es la línea que había roto. La restauro.
        self.search_results_tree.bind("<Double-1>", self.add_to_cart_event)

        # --- Columna Derecha: Carrito de Venta ---
        right_frame = ttk.Frame(self, style="Card.TFrame", padding=20)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(2, weight=1) # La tabla del carrito se expande

        # Sección del Cliente
        client_section_frame = ttk.Frame(right_frame, style="Card.TFrame")
        client_section_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        client_section_frame.columnconfigure(0, weight=1)
        self.select_client_button = ttk.Button(client_section_frame, text="Seleccionar Cliente")
        self.select_client_button.grid(row=0, column=1, sticky="e")
        self.selected_client_var = tk.StringVar(value="Cliente: Público General")
        ttk.Label(client_section_frame, textvariable=self.selected_client_var, font=("Segoe UI", 10, "italic")).grid(row=0, column=0, sticky="w")
        
        # Carrito
        ttk.Label(right_frame, text="Venta Actual", font=("Segoe UI", 16, "bold")).grid(row=1, column=0, sticky="w", pady=(0, 10))
        
        self.cart_tree = ttk.Treeview(right_frame, columns=("id", "qty", "nombre", "precio_unit", "subtotal"), show="headings", displaycolumns=("qty", "nombre", "precio_unit", "subtotal"))
        self.cart_tree.heading("qty", text="Cant.")
        self.cart_tree.heading("nombre", text="Producto")
        self.cart_tree.heading("precio_unit", text="P. Unit.")
        self.cart_tree.heading("subtotal", text="Subtotal")
        self.cart_tree.column("qty", width=50, anchor=tk.CENTER)
        self.cart_tree.column("precio_unit", width=80, anchor=tk.E)
        self.cart_tree.column("subtotal", width=90, anchor=tk.E)
        self.cart_tree.grid(row=2, column=0, sticky="nsew", pady=5)

        # Botones de control del carrito
        cart_controls_frame = ttk.Frame(right_frame, style="Card.TFrame")
        cart_controls_frame.grid(row=3, column=0, sticky="e", pady=(5,0))
        self.increase_qty_button = ttk.Button(cart_controls_frame, text="+")
        self.increase_qty_button.pack(side="left")
        self.decrease_qty_button = ttk.Button(cart_controls_frame, text="-")
        self.decrease_qty_button.pack(side="left", padx=5)
        self.remove_item_button = ttk.Button(cart_controls_frame, text="Eliminar")
        self.remove_item_button.pack(side="left")
        
        # Totales
        total_frame = ttk.Frame(right_frame, style="Card.TFrame")
        total_frame.grid(row=4, column=0, sticky="ew", pady=10)
        total_frame.columnconfigure(1, weight=1)
        ttk.Label(total_frame, text="TOTAL:", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, sticky="w", padx=5)
        self.total_var = tk.StringVar(value="S/ 0.00")
        ttk.Label(total_frame, textvariable=self.total_var, font=("Segoe UI", 18, "bold"), anchor="e").grid(row=0, column=1, sticky="e", padx=5)
        
        # Botones de acción final
        action_buttons_frame = ttk.Frame(right_frame)
        action_buttons_frame.grid(row=5, column=0, sticky="ew")
        action_buttons_frame.columnconfigure(0, weight=1)
        action_buttons_frame.columnconfigure(1, weight=1)
        self.complete_sale_button = ttk.Button(action_buttons_frame, text="Finalizar Venta", style="Accent.TButton")
        self.complete_sale_button.grid(row=0, column=1, sticky="ew", ipady=10, padx=(5,0))
        self.cancel_sale_button = ttk.Button(action_buttons_frame, text="Cancelar")
        self.cancel_sale_button.grid(row=0, column=0, sticky="ew", ipady=10, padx=(0,5))

    def set_controller(self, controller):
        self.controller = controller
        self.select_client_button.config(command=self.controller.show_client_search_popup)
        self.complete_sale_button.config(command=self.controller.process_sale)
        self.cancel_sale_button.config(command=self.controller.clear_sale)
        self.increase_qty_button.config(command=self.controller.increase_cart_item_qty)
        self.decrease_qty_button.config(command=self.controller.decrease_cart_item_qty)
        self.remove_item_button.config(command=self.controller.remove_cart_item)

    def on_key_release(self, event):
        search_term = self.search_var.get()
        self.controller.search_products_for_sale(search_term)

    def add_to_cart_event(self, event):
        selected_item = self.search_results_tree.focus()
        if selected_item:
            # Aseguramos que el ID esté en la columna correcta
            item_values = self.search_results_tree.item(selected_item, "values")
            product_id = item_values[3]
            self.controller.add_product_to_cart(int(product_id))

    def get_selected_cart_item_id(self):
        selection = self.cart_tree.selection()
        if selection:
            return int(self.cart_tree.item(selection[0])['values'][0])
        return None
