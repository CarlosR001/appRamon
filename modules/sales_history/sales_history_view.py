import tkinter as tk
from tkinter import ttk
from datetime import datetime

try:
    from tkcalendar import DateEntry
    calendar_available = True
except ImportError:
    calendar_available = False

class SalesHistoryView(ttk.Frame):
    def __init__(self, parent, is_admin):
        super().__init__(parent, padding=10)
        self.controller = None
        self.is_admin = is_admin

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.create_header_and_filters()
        self.create_sales_treeview()
        self.create_action_buttons()

    def set_controller(self, controller):
        self.controller = controller
        if calendar_available:
            self.filter_button.config(command=self.controller.load_sales_history)
        self.reprint_button.config(command=self.controller.reprint_receipt)
        self.void_button.config(command=self.controller.void_sale)

    def create_header_and_filters(self):
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        title = ttk.Label(header_frame, text="Historial de Ventas", font=("Segoe UI", 16, "bold"))
        title.pack(side="left", padx=(0, 20))

        if calendar_available:
            ttk.Label(header_frame, text="Desde:").pack(side="left", padx=(0, 5))
            self.start_date_entry = DateEntry(header_frame, date_pattern='dd/mm/yyyy', width=12)
            self.start_date_entry.pack(side="left")
            ttk.Label(header_frame, text="Hasta:").pack(side="left", padx=(10, 5))
            self.end_date_entry = DateEntry(header_frame, date_pattern='dd/mm/yyyy', width=12)
            self.end_date_entry.pack(side="left")
            self.filter_button = ttk.Button(header_frame, text="Filtrar")
            self.filter_button.pack(side="left", padx=10)

    def create_sales_treeview(self):
        tree_frame = ttk.Frame(self)
        tree_frame.grid(row=1, column=0, sticky="nsew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_frame, columns=("id", "fecha", "cliente", "vendedor", "total", "estado"), show="headings")
        self.tree.heading("id", text="ID Venta"); self.tree.heading("fecha", text="Fecha"); self.tree.heading("cliente", text="Cliente");
        self.tree.heading("vendedor", text="Vendedor"); self.tree.heading("total", text="Total"); self.tree.heading("estado", text="Estado")
        self.tree.column("id", width=60, anchor="c"); self.tree.column("fecha", width=140); self.tree.column("cliente", width=200);
        self.tree.column("vendedor", width=120); self.tree.column("total", width=90, anchor="e"); self.tree.column("estado", width=90, anchor="c")
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def create_action_buttons(self):
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, sticky="w", pady=(10, 0))
        
        self.reprint_button = ttk.Button(button_frame, text="Reimprimir Ticket")
        self.reprint_button.pack(side="left")

        # El botón de anular solo está disponible para administradores
        void_state = tk.NORMAL if self.is_admin else tk.DISABLED
        self.void_button = ttk.Button(button_frame, text="Anular Venta", state=void_state)
        self.void_button.pack(side="left", padx=10)

    def get_selected_sale_id(self):
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0], "values")[0]
        return None

    def clear_tree(self):
        self.tree.delete(*self.tree.get_children())

    def insert_sale(self, sale):
        fecha = sale.get('fecha')
        if isinstance(fecha, datetime):
            fecha = fecha.strftime('%d/%m/%Y %H:%M')
        
        self.tree.insert("", "end", iid=sale['id'], values=(
            sale['id'], fecha,
            sale.get('cliente_nombre', 'Público General'),
            sale.get('nombre_usuario', 'N/A'),
            f"S/ {sale.get('total', 0.0):.2f}",
            sale.get('estado', 'Completada')
        ))
