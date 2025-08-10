import tkinter as tk
from tkinter import ttk
from datetime import datetime

class ServicesView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.controller = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.create_header()
        self.create_services_treeview()
        self.create_action_buttons()

    def set_controller(self, controller):
        self.controller = controller
        self.add_button.config(command=self.controller.show_add_service_window)
        self.edit_button.config(command=self.controller.show_update_service_window)
        self.details_button.config(command=self.controller.show_service_details_popup)

    def create_header(self):
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        title = ttk.Label(header_frame, text="Gestión de Servicios y Reparaciones", font=("Segoe UI", 16, "bold"))
        title.pack(side="left")

    def create_services_treeview(self):
        tree_frame = ttk.Frame(self)
        tree_frame.grid(row=1, column=0, sticky="nsew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_frame, columns=("id", "cliente", "equipo", "estado", "fecha"), show="headings")
        self.tree.heading("id", text="ID Orden")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("equipo", text="Equipo")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("fecha", text="Fecha Recepción")
        self.tree.column("id", width=80, anchor=tk.CENTER)
        self.tree.column("cliente", width=200)
        self.tree.column("equipo", width=250)
        self.tree.column("estado", width=120, anchor=tk.CENTER)
        self.tree.column("fecha", width=150, anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def create_action_buttons(self):
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, sticky="w", pady=(10, 0))
        
        self.add_button = ttk.Button(button_frame, text="Registrar Nuevo Servicio", style="Accent.TButton")
        self.add_button.pack(side="left", padx=(0, 5))

        self.edit_button = ttk.Button(button_frame, text="Gestionar/Actualizar")
        self.edit_button.pack(side="left", padx=5)

        self.details_button = ttk.Button(button_frame, text="Ver Detalles (Solo Lectura)")
        self.details_button.pack(side="left", padx=5)

    def get_selected_service_id(self):
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0], "values")[0]
        return None

    def clear_tree(self):
        self.tree.delete(*self.tree.get_children())

    def insert_service(self, service):
        fecha = service.get('fecha_recepcion')
        if isinstance(fecha, datetime):
            fecha = fecha.strftime('%d/%m/%Y %H:%M')

        estado = service.get('estado', 'Desconocido')
        
        self.tree.insert("", "end", iid=service['id'], values=(
            service['id'],
            service.get('nombre_cliente', 'N/A'),
            service.get('descripcion_equipo', ''),
            estado,
            fecha
        ))
