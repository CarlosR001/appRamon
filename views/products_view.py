import tkinter as tk
from tkinter import ttk, messagebox

class ProductsView(ttk.Frame):
    def __init__(self, parent, user_role):
        super().__init__(parent)
        self.user_role = user_role
        self.is_admin = (self.user_role == 1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.create_header()
        self.create_product_treeview()
        self.create_action_buttons()

    def create_header(self):
        """Crea el encabezado con título, campo de búsqueda y botones."""
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.columnconfigure(1, weight=1) # Permite que la barra de búsqueda se expanda

        title = ttk.Label(header_frame, text="Gestión de Productos", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, sticky="w", padx=(0, 20))

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(header_frame, textvariable=self.search_var, width=50)
        search_entry.grid(row=0, column=1, sticky="ew")
        search_entry.bind("<Return>", lambda event: self.search_button.invoke()) # Buscar al presionar Enter

        self.search_button = ttk.Button(header_frame, text="Buscar")
        self.search_button.grid(row=0, column=2, sticky="e", padx=5)

        self.clear_button = ttk.Button(header_frame, text="Limpiar")
        self.clear_button.grid(row=0, column=3, sticky="e")

    def create_product_treeview(self):
        tree_frame = ttk.Frame(self)
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        columns = ("id", "codigo", "nombre", "precio_venta", "stock", "categoria")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombre", text="Nombre del Producto")
        self.tree.heading("precio_venta", text="Precio Venta")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("categoria", text="Categoría")
        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("codigo", width=120)
        self.tree.column("nombre", width=350)
        self.tree.column("precio_venta", width=100, anchor=tk.E)
        self.tree.column("stock", width=80, anchor=tk.CENTER)
        self.tree.column("categoria", width=150)
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def create_action_buttons(self):
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        # --- Botones de la izquierda ---
        left_button_frame = ttk.Frame(button_frame)
        left_button_frame.pack(side="left")

        self.add_button = ttk.Button(left_button_frame, text="Añadir Producto", style="Accent.TButton")
        self.add_button.pack(side="left", padx=(0, 5))

        edit_state = tk.NORMAL if self.is_admin else tk.DISABLED
        self.edit_button = ttk.Button(left_button_frame, text="Editar Producto", state=edit_state)
        self.edit_button.pack(side="left", padx=5)

        delete_state = tk.NORMAL if self.is_admin else tk.DISABLED
        self.delete_button = ttk.Button(left_button_frame, text="Eliminar Producto", state=delete_state)
        self.delete_button.pack(side="left", padx=5)

        # --- Botones de la derecha ---
        right_button_frame = ttk.Frame(button_frame)
        right_button_frame.pack(side="right")

        category_state = tk.NORMAL if self.is_admin else tk.DISABLED
        self.manage_categories_button = ttk.Button(right_button_frame, text="Gestionar Categorías", state=category_state)
        self.manage_categories_button.pack(side="right")

    def set_controller(self, controller):
        """Asigna el controlador a los comandos de los botones."""
        self.add_button.config(command=controller.show_add_product_window)
        self.search_button.config(command=controller.search_products)
        self.clear_button.config(command=controller.clear_search)
        
        if self.is_admin:
            self.edit_button.config(command=controller.show_edit_product_window)
            self.delete_button.config(command=controller.delete_selected_product)
            self.manage_categories_button.config(command=controller.show_categories_manager)
        
    def add_product_to_tree(self, product):
        precio_formateado = f"S/ {product.get('precio_venta', 0.0):.2f}"
        self.tree.insert("", tk.END, iid=product['id'], values=(
            product['id'],
            product.get('codigo', ''),
            product.get('nombre', ''),
            precio_formateado,
            product.get('stock', 0),
            product.get('categoria', 'N/A')
        ))
    
    def get_selected_item_id(self):
        selection = self.tree.selection()
        if selection:
            return int(self.tree.item(selection[0])['values'][0])
        return None

    def clear_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
