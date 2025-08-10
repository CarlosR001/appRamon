import tkinter as tk
from tkinter import ttk, messagebox

class ProductsView(ttk.Frame):
    def __init__(self, parent, user_role):
        super().__init__(parent)
        self.user_role = user_role

        # Configurar el layout del frame principal
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Crear widgets
        self.create_header()
        self.create_product_treeview()
        self.create_action_buttons()

    def create_header(self):
        """Crea el encabezado con el título y el botón de búsqueda."""
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        title = ttk.Label(header_frame, text="Gestión de Productos", font=("Arial", 16, "bold"))
        title.pack(side="left")

        # Aquí se podrían añadir widgets de búsqueda en el futuro
        # search_entry = ttk.Entry(header_frame)
        # search_entry.pack(side="right")
        # search_button = ttk.Button(header_frame, text="Buscar")
        # search_button.pack(side="right", padx=5)

    def create_product_treeview(self):
        """Crea la tabla (Treeview) para mostrar los productos."""
        tree_frame = ttk.Frame(self)
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        columns = ("id", "codigo", "nombre", "precio_venta", "stock", "categoria")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        # Definir encabezados
        self.tree.heading("id", text="ID")
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("precio_venta", text="Precio Venta")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("categoria", text="Categoría")

        # Configurar el ancho de las columnas
        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("codigo", width=120)
        self.tree.column("nombre", width=300)
        self.tree.column("precio_venta", width=100, anchor=tk.E)
        self.tree.column("stock", width=80, anchor=tk.CENTER)
        self.tree.column("categoria", width=150)

        # Añadir scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def create_action_buttons(self):
        """Crea los botones de acción (Añadir, Editar, Eliminar)."""
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Estos botones solo deberían estar habilitados para el Administrador
        # En el futuro, la lógica de habilitación/deshabilitación irá aquí.
        
        self.add_button = ttk.Button(button_frame, text="Añadir Producto")
        self.add_button.pack(side="left", padx=5)

        self.edit_button = ttk.Button(button_frame, text="Editar Producto")
        self.edit_button.pack(side="left", padx=5)

        self.delete_button = ttk.Button(button_frame, text="Eliminar Producto")
        self.delete_button.pack(side="left", padx=5)

    def set_controller(self, controller):
        """Asigna el controlador a los comandos de los botones."""
        self.add_button.config(command=controller.show_add_product_window)
        # Los comandos de editar y eliminar se añadirán más adelante
        # self.edit_button.config(command=controller.show_edit_product_window)
        # self.delete_button.config(command=controller.delete_product)
        
    def add_product_to_tree(self, product):
        """Añade un nuevo producto a la tabla."""
        # El formato del precio se hará aquí para la visualización
        precio_formateado = f"S/ {product['precio_venta']:.2f}"
        self.tree.insert("", tk.END, values=(
            product['id'],
            product['codigo'],
            product['nombre'],
            precio_formateado,
            product['stock'],
            product['categoria']
        ))
    
    def clear_tree(self):
        """Limpia todos los datos de la tabla."""
        for i in self.tree.get_children():
            self.tree.delete(i)
