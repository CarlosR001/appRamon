import tkinter as tk
from tkinter import ttk, messagebox

class ProductsView(ttk.Frame):
    def __init__(self, parent, user_role):
        super().__init__(parent)
        self.user_role = user_role

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.create_header()
        self.create_product_treeview()
        self.create_action_buttons()

    def create_header(self):
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        title = ttk.Label(header_frame, text="Gestión de Productos", font=("Segoe UI", 16, "bold"))
        title.pack(side="left")

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
        button_frame.grid(row=2, column=0, sticky="w", padx=10, pady=(0, 10))
        
        self.add_button = ttk.Button(button_frame, text="Añadir Producto", style="Accent.TButton")
        self.add_button.pack(side="left", padx=(0, 5))

        self.edit_button = ttk.Button(button_frame, text="Editar Producto")
        self.edit_button.pack(side="left", padx=5)

        self.delete_button = ttk.Button(button_frame, text="Eliminar Producto")
        self.delete_button.pack(side="left", padx=5)

    def set_controller(self, controller):
        """Asigna el controlador a los comandos de los botones."""
        self.add_button.config(command=controller.show_add_product_window)
        self.edit_button.config(command=controller.show_edit_product_window)
        self.delete_button.config(command=controller.delete_selected_product)
        
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
        """Devuelve el ID del item seleccionado en el treeview."""
        selection = self.tree.selection()
        if selection:
            return int(self.tree.item(selection[0])['values'][0])
        return None

    def clear_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
