import tkinter as tk
from tkinter import ttk

class SalesView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # --- Layout Principal (2 columnas) ---
        self.columnconfigure(0, weight=1) # Columna de búsqueda
        self.columnconfigure(1, weight=2) # Columna del carrito (más ancha)
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
        search_entry.bind("<KeyRelease>", self.on_key_release) # Buscar mientras se escribe

        # Tabla para mostrar resultados de búsqueda
        self.search_results_tree = ttk.Treeview(left_frame, columns=("nombre", "precio", "stock"), show="headings")
        self.search_results_tree.heading("nombre", text="Producto")
        self.search_results_tree.heading("precio", text="Precio")
        self.search_results_tree.heading("stock", text="Stock")
        self.search_results_tree.column("precio", width=80, anchor=tk.E)
        self.search_results_tree.column("stock", width=60, anchor=tk.CENTER)
        self.search_results_tree.grid(row=1, column=0, sticky="nsew")
        self.search_results_tree.bind("<Double-1>", self.add_to_cart_event) # Añadir con doble clic

        # --- Columna Derecha: Carrito de Venta ---
        right_frame = ttk.Frame(self, style="Card.TFrame", padding=20)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)

        ttk.Label(right_frame, text="Venta Actual", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # Tabla para el carrito
        self.cart_tree = ttk.Treeview(right_frame, columns=("qty", "nombre", "precio_unit", "subtotal"), show="headings")
        self.cart_tree.heading("qty", text="Cant.")
        self.cart_tree.heading("nombre", text="Producto")
        self.cart_tree.heading("precio_unit", text="P. Unit.")
        self.cart_tree.heading("subtotal", text="Subtotal")
        self.cart_tree.column("qty", width=50, anchor=tk.CENTER)
        self.cart_tree.column("precio_unit", width=80, anchor=tk.E)
        self.cart_tree.column("subtotal", width=90, anchor=tk.E)
        self.cart_tree.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=5)
        
        # Frame para los totales
        total_frame = ttk.Frame(right_frame, style="Card.TFrame")
        total_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        total_frame.columnconfigure(1, weight=1)

        ttk.Label(total_frame, text="TOTAL:", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, sticky="w", padx=5)
        self.total_var = tk.StringVar(value="S/ 0.00")
        ttk.Label(total_frame, textvariable=self.total_var, font=("Segoe UI", 18, "bold"), anchor="e").grid(row=0, column=1, sticky="e", padx=5)
        
        # Frame para botones de acción
        action_buttons_frame = ttk.Frame(right_frame)
        action_buttons_frame.grid(row=3, column=0, columnspan=2, sticky="ew")
        action_buttons_frame.columnconfigure(0, weight=1)
        action_buttons_frame.columnconfigure(1, weight=1)

        self.complete_sale_button = ttk.Button(action_buttons_frame, text="Finalizar Venta", style="Accent.TButton")
        self.complete_sale_button.grid(row=0, column=1, sticky="ew", ipady=10, padx=(5,0))

        self.cancel_sale_button = ttk.Button(action_buttons_frame, text="Cancelar")
        self.cancel_sale_button.grid(row=0, column=0, sticky="ew", ipady=10, padx=(0,5))

    def set_controller(self, controller):
        """Asigna los controladores a los eventos de los widgets."""
        self.controller = controller
        self.complete_sale_button.config(command=self.controller.process_sale)
        self.cancel_sale_button.config(command=self.controller.clear_sale)

    def on_key_release(self, event):
        """Llama al controlador para buscar productos mientras se escribe."""
        search_term = self.search_var.get()
        self.controller.search_products_for_sale(search_term)

    def add_to_cart_event(self, event):
        """Llama al controlador para añadir el producto seleccionado al carrito."""
        selected_item = self.search_results_tree.focus()
        if selected_item:
            product_id = self.search_results_tree.item(selected_item, "values")[3] # ID oculto
            self.controller.add_product_to_cart(int(product_id))
