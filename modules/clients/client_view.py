import tkinter as tk
from tkinter import ttk

class ClientsView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.controller = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.create_header()
        self.create_client_treeview()
        self.create_action_buttons()

    def set_controller(self, controller):
        self.controller = controller
        self.search_button.config(command=self.controller.search_clients)
        self.clear_button.config(command=self.controller.load_all_clients)
        self.add_button.config(command=self.controller.show_add_client_window)
        self.edit_button.config(command=self.controller.show_edit_client_window)
        self.delete_button.config(command=self.controller.delete_client)

    def create_header(self):
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)

        title = ttk.Label(header_frame, text="Gestión de Clientes", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, sticky="w", padx=(0, 20))

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(header_frame, textvariable=self.search_var, width=50)
        search_entry.grid(row=0, column=1, sticky="ew")
        search_entry.bind("<Return>", lambda event: self.search_button.invoke())

        self.search_button = ttk.Button(header_frame, text="Buscar")
        self.search_button.grid(row=0, column=2, sticky="e", padx=5)

        self.clear_button = ttk.Button(header_frame, text="Limpiar")
        self.clear_button.grid(row=0, column=3, sticky="e")

    def create_client_treeview(self):
        tree_frame = ttk.Frame(self)
        tree_frame.grid(row=1, column=0, sticky="nsew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_frame, columns=("id", "nombre", "telefono", "email"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre del Cliente")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("email", text="Email")

        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("nombre", width=250)
        self.tree.column("telefono", width=120)
        self.tree.column("email", width=250)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def create_action_buttons(self):
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, sticky="w", pady=(10, 0))
        
        self.add_button = ttk.Button(button_frame, text="Añadir Cliente", style="Accent.TButton")
        self.add_button.pack(side="left", padx=(0, 5))

        self.edit_button = ttk.Button(button_frame, text="Editar Cliente")
        self.edit_button.pack(side="left", padx=5)

        self.delete_button = ttk.Button(button_frame, text="Eliminar Cliente")
        self.delete_button.pack(side="left", padx=5)

    def get_selected_client_id(self):
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0], "values")[0]
        return None

    def clear_tree(self):
        self.tree.delete(*self.tree.get_children())

    def insert_client(self, client):
        self.tree.insert("", tk.END, iid=client['id'], values=(
            client['id'],
            client.get('nombre', ''),
            client.get('telefono', ''),
            client.get('email', '')
        ))
