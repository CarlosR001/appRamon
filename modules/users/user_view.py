import tkinter as tk
from tkinter import ttk, messagebox

class UserView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)
        self.controller = None
        self.roles = [] # Se llenará desde el controlador

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.create_add_user_form()
        self.create_user_treeview()

    def set_controller(self, controller):
        self.controller = controller
        self.add_button.config(command=self.controller.add_user)
        self.delete_button.config(command=self.controller.delete_user)

    def set_roles(self, roles):
        """Recibe la lista de roles desde el controlador."""
        self.roles = roles
        self.role_combobox['values'] = [role['nombre_rol'] for role in self.roles]

    def create_add_user_form(self):
        form_frame = ttk.LabelFrame(self, text="Crear Nuevo Usuario", padding=10)
        form_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        form_frame.columnconfigure(1, weight=1)

        # Nombre Completo
        ttk.Label(form_frame, text="Nombre Completo:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.full_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.full_name_var).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Nombre de Usuario
        ttk.Label(form_frame, text="Usuario:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.username_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.username_var).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Contraseña
        ttk.Label(form_frame, text="Contraseña:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.password_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.password_var, show="*").grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Rol
        ttk.Label(form_frame, text="Rol:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.role_var = tk.StringVar()
        self.role_combobox = ttk.Combobox(form_frame, textvariable=self.role_var, state="readonly")
        self.role_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Botón
        self.add_button = ttk.Button(form_frame, text="Crear Usuario", style="Accent.TButton")
        self.add_button.grid(row=4, column=0, columnspan=2, pady=(10,0), ipady=4, sticky="ew")

    def create_user_treeview(self):
        list_frame = ttk.Frame(self)
        list_frame.grid(row=1, column=0, sticky="nsew")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)
        
        self.delete_button = ttk.Button(list_frame, text="Eliminar Usuario Seleccionado")
        self.delete_button.pack(anchor="e", pady=(0,5))
        
        tree_container = ttk.Frame(list_frame)
        tree_container.pack(fill="both", expand=True)
        tree_container.columnconfigure(0, weight=1)
        tree_container.rowconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(tree_container, columns=("id", "usuario", "nombre_completo", "rol"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("usuario", text="Usuario")
        self.tree.heading("nombre_completo", text="Nombre Completo")
        self.tree.heading("rol", text="Rol")
        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("usuario", width=150)
        self.tree.column("nombre_completo", width=250)
        self.tree.column("rol", width=120, anchor=tk.CENTER)
        scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def get_user_data(self):
        """Recupera y valida los datos del formulario de nuevo usuario."""
        full_name = self.full_name_var.get()
        username = self.username_var.get()
        password = self.password_var.get()
        role_name = self.role_var.get()

        if not all([full_name, username, password, role_name]):
            messagebox.showwarning("Campos Incompletos", "Todos los campos son obligatorios.", parent=self)
            return None
            
        # Encontrar el ID del rol seleccionado
        role_id = next((r['id'] for r in self.roles if r['nombre_rol'] == role_name), None)
        if role_id is None:
            messagebox.showerror("Error de Rol", "El rol seleccionado no es válido.", parent=self)
            return None
            
        return {
            'nombre_completo': full_name,
            'nombre_usuario': username,
            'password': password,
            'id_rol': role_id
        }

    def get_selected_user_id(self):
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0], "values")[0]
        return None

    def clear_form(self):
        self.full_name_var.set("")
        self.username_var.set("")
        self.password_var.set("")
        self.role_var.set("")

    def clear_tree(self):
        self.tree.delete(*self.tree.get_children())

    def insert_user(self, user):
        self.tree.insert("", "end", iid=user['id'], values=(
            user['id'],
            user.get('nombre_usuario', ''),
            user.get('nombre_completo', ''),
            user.get('nombre_rol', '')
        ))
