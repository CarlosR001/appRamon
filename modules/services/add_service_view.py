import tkinter as tk
from tkinter import ttk, messagebox

class AddServiceView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # --- Window Setup ---
        self.title("Registrar Nuevo Servicio")
        self.geometry("500x550")
        self.resizable(False, False)
        self.grab_set()

        # --- Main Frame ---
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(expand=True, fill="both")

        # --- Client Selection ---
        client_frame = ttk.LabelFrame(main_frame, text="1. Buscar y Seleccionar Cliente", padding=10)
        client_frame.pack(fill="x", pady=(0, 15))
        client_frame.columnconfigure(0, weight=1)
        
        self.client_search_var = tk.StringVar()
        client_search_entry = ttk.Entry(client_frame, textvariable=self.client_search_var)
        client_search_entry.grid(row=0, column=0, sticky="ew", padx=(0,5))
        client_search_entry.bind("<KeyRelease>", self.search_client_event)

        # --- Client Search Results ---
        self.client_tree = ttk.Treeview(client_frame, columns=("id", "nombre", "telefono"), show="headings", height=4)
        self.client_tree.heading("id", text="ID")
        self.client_tree.heading("nombre", text="Nombre")
        self.client_tree.heading("telefono", text="Teléfono")
        self.client_tree.column("id", width=50, anchor=tk.CENTER)
        self.client_tree.grid(row=1, column=0, sticky="nsew", pady=(5,0))
        self.client_tree.bind("<<TreeviewSelect>>", self.on_client_select_event)

        # --- Selected Client Display ---
        self.selected_client_var = tk.StringVar(value="Ningún cliente seleccionado.")
        ttk.Label(client_frame, textvariable=self.selected_client_var, font=("Segoe UI", 9, "italic")).grid(row=2, column=0, sticky="w", pady=(5,0))
        self.selected_client_id = None

        # --- Service Details ---
        details_frame = ttk.LabelFrame(main_frame, text="2. Detalles del Servicio", padding=10)
        details_frame.pack(fill="x")
        details_frame.columnconfigure(1, weight=1)

        ttk.Label(details_frame, text="Equipo:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.equipo_entry = ttk.Entry(details_frame)
        self.equipo_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(details_frame, text="Problema Reportado:").grid(row=1, column=0, sticky="nw", padx=5, pady=5)
        self.problema_text = tk.Text(details_frame, height=6)
        self.problema_text.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # --- Action Buttons ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side="bottom", fill="x", pady=(15, 0))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        self.save_button = ttk.Button(button_frame, text="Guardar Orden de Servicio", style="Accent.TButton", command=self.save)
        self.save_button.grid(row=0, column=1, sticky="e")
        
        self.cancel_button = ttk.Button(button_frame, text="Cancelar", command=self.destroy)
        self.cancel_button.grid(row=0, column=0, sticky="w")
        
    def search_client_event(self, event):
        """Notifica al controlador que se debe buscar un cliente."""
        search_term = self.client_search_var.get()
        self.controller.search_clients_for_service(search_term)

    def on_client_select_event(self, event):
        """Notifica al controlador que un cliente ha sido seleccionado."""
        selection = self.client_tree.selection()
        if selection:
            item = self.client_tree.item(selection[0], "values")
            self.selected_client_id = item[0]
            self.selected_client_var.set(f"Seleccionado: {item[1]}")

    def update_client_list(self, clients):
        """Limpia y rellena la lista de resultados de búsqueda de clientes."""
        self.client_tree.delete(*self.client_tree.get_children())
        for client in clients:
            self.client_tree.insert("", "end", values=(client['id'], client['nombre'], client['telefono']))

    def save(self):
        """Recopila los datos y los envía al controlador para ser guardados."""
        if not self.selected_client_id:
            messagebox.showwarning("Cliente no seleccionado", "Por favor, busque y seleccione un cliente.", parent=self)
            return
            
        data = {
            'id_cliente': self.selected_client_id,
            'descripcion_equipo': self.equipo_entry.get(),
            'problema_reportado': self.problema_text.get("1.0", tk.END).strip()
        }

        if not data['descripcion_equipo'] or not data['problema_reportado']:
            messagebox.showwarning("Campos Requeridos", "La descripción del equipo y el problema reportado son obligatorios.", parent=self)
            return

        self.controller.add_service(data)
        self.destroy()
