import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class UserView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)
        self.controller = None
        self.roles = []
        self.permissions = []
        self.permission_vars = {}

        self.columnconfigure(0, weight=1); self.rowconfigure(0, weight=1)

        # --- Notebook para las Pestañas ---
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        # --- Pestaña 1: Gestionar Usuarios ---
        users_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(users_frame, text="Gestionar Usuarios")
        self.create_users_tab(users_frame)

        # --- Pestaña 2: Gestionar Roles y Permisos ---
        roles_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(roles_frame, text="Gestionar Roles y Permisos")
        self.create_roles_tab(roles_frame)

    def set_controller(self, controller):
        self.controller = controller
        self.add_user_button.config(command=self.controller.add_user)
        self.edit_user_button.config(command=self.controller.edit_user)
        self.delete_user_button.config(command=self.controller.delete_user)
        self.role_select_combo.bind("<<ComboboxSelected>>", self.controller.on_role_selected)
        self.save_permissions_button.config(command=self.controller.save_role_permissions)

    # --- PESTAÑA 1: GESTIONAR USUARIOS ---
    def create_users_tab(self, parent_frame):
        parent_frame.columnconfigure(0, weight=1); parent_frame.rowconfigure(1, weight=1)
        
        # Formulario para añadir/editar
        form = ttk.LabelFrame(parent_frame, text="Añadir/Editar Usuario", padding=10)
        form.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        form.columnconfigure(1, weight=1)
        self.user_form_fields = {
            "full_name": tk.StringVar(), "username": tk.StringVar(), 
            "password": tk.StringVar(), "role": tk.StringVar()
        }
        ttk.Label(form, text="Nombre Completo:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(form, textvariable=self.user_form_fields["full_name"]).grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        ttk.Label(form, text="Usuario:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(form, textvariable=self.user_form_fields["username"]).grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        ttk.Label(form, text="Contraseña:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.password_entry = ttk.Entry(form, textvariable=self.user_form_fields["password"], show="*")
        self.password_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        ttk.Label(form, text="Rol:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.user_role_combo = ttk.Combobox(form, textvariable=self.user_form_fields["role"], state="readonly")
        self.user_role_combo.grid(row=3, column=1, sticky="ew", padx=5, pady=2)
        
        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(10,0))
        self.add_user_button = ttk.Button(btn_frame, text="Añadir Nuevo", style="Accent.TButton")
        self.add_user_button.pack(side="left")
        self.edit_user_button = ttk.Button(btn_frame, text="Guardar Cambios")
        self.edit_user_button.pack(side="left", padx=5)

        # Lista de usuarios
        list_frame = ttk.Frame(parent_frame)
        list_frame.grid(row=1, column=0, sticky="nsew")
        list_frame.columnconfigure(0, weight=1); list_frame.rowconfigure(0, weight=1)
        self.delete_user_button = ttk.Button(list_frame, text="Eliminar Usuario Seleccionado")
        self.delete_user_button.pack(anchor="e", pady=(0,5))
        self.user_tree = ttk.Treeview(list_frame, columns=("id", "usuario", "nombre_completo", "rol"), show="headings")
        self.user_tree.heading("id", text="ID"); self.user_tree.heading("usuario", text="Usuario"); self.user_tree.heading("nombre_completo", text="Nombre Completo"); self.user_tree.heading("rol", text="Rol")
        self.user_tree.column("id", width=50, anchor="c"); self.user_tree.column("usuario", width=150); self.user_tree.column("nombre_completo", width=250); self.user_tree.column("rol", width=120, anchor="c")
        self.user_tree.pack(fill="both", expand=True)
        self.user_tree.bind("<<TreeviewSelect>>", self.on_user_select)

    # --- PESTAÑA 2: GESTIONAR ROLES Y PERMISOS ---
    def create_roles_tab(self, parent_frame):
        parent_frame.columnconfigure(0, weight=1); parent_frame.rowconfigure(1, weight=1)
        
        # Selector de Rol
        top_frame = ttk.Frame(parent_frame)
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ttk.Label(top_frame, text="Seleccionar Rol a Editar:").pack(side="left", padx=(0,10))
        self.role_select_var = tk.StringVar()
        self.role_select_combo = ttk.Combobox(top_frame, textvariable=self.role_select_var, state="readonly")
        self.role_select_combo.pack(fill="x", expand=True, side="left")
        
        # Canvas y Frame para checkboxes con scroll
        canvas_frame = ttk.Frame(parent_frame)
        canvas_frame.grid(row=1, column=0, sticky="nsew")
        canvas_frame.columnconfigure(0, weight=1); canvas_frame.rowconfigure(0, weight=1)
        canvas = tk.Canvas(canvas_frame); canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)
        self.permissions_frame = ttk.Frame(canvas, padding=10)
        canvas.create_window((0,0), window=self.permissions_frame, anchor="nw")
        self.permissions_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Botón de Guardar
        self.save_permissions_button = ttk.Button(parent_frame, text="Guardar Permisos para este Rol", style="Accent.TButton")
        self.save_permissions_button.grid(row=2, column=0, sticky="e", pady=(10,0))

    # --- MÉTODOS DE LA VISTA ---
    def set_roles(self, roles):
        self.roles = roles
        role_names = [r['nombre_rol'] for r in roles]
        self.user_role_combo['values'] = role_names
        self.role_select_combo['values'] = role_names

    def populate_permissions(self, all_permissions, role_permissions):
        self.permission_vars.clear()
        for widget in self.permissions_frame.winfo_children(): widget.destroy()
        
        for p in all_permissions:
            var = tk.BooleanVar(value=(p['id'] in role_permissions))
            self.permission_vars[p['id']] = var
            cb = ttk.Checkbutton(self.permissions_frame, text=p['descripcion'], variable=var)
            cb.pack(anchor="w", pady=2)

    def on_user_select(self, event=None):
        selection = self.user_tree.selection()
        if not selection: return
        item = self.user_tree.item(selection[0], "values")
        # ID, usuario, nombre_completo, rol
        self.user_form_fields["full_name"].set(item[2])
        self.user_form_fields["username"].set(item[1])
        self.user_form_fields["role"].set(item[3])
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, "********")

    def get_user_data(self, is_edit=False):
        data = { "nombre_completo": self.user_form_fields["full_name"].get(),
                 "nombre_usuario": self.user_form_fields["username"].get(),
                 "password": self.user_form_fields["password"].get() }
        role_name = self.user_form_fields["role"].get()
        role_id = next((r['id'] for r in self.roles if r['nombre_rol'] == role_name), None)

        if not all([data["nombre_completo"], data["nombre_usuario"], role_id]):
            messagebox.showwarning("Campos Incompletos", "Nombre Completo, Usuario y Rol son requeridos.", parent=self); return None
        if not is_edit and not data["password"]:
            messagebox.showwarning("Campos Incompletos", "La contraseña es requerida para nuevos usuarios.", parent=self); return None
        
        data['id_rol'] = role_id
        return data

    def get_selected_user_id(self):
        selection = self.user_tree.selection()
        if selection: return self.user_tree.item(selection[0], "values")[0]
        return None

    def clear_user_form(self):
        for var in self.user_form_fields.values(): var.set("")

    def insert_user(self, user):
        self.user_tree.insert("", "end", iid=user['id'], values=(user['id'], user.get('nombre_usuario', ''), user.get('nombre_completo', ''), user.get('nombre_rol', '')))

    def clear_user_tree(self):
        self.user_tree.delete(*self.user_tree.get_children())
