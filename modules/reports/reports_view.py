import tkinter as tk
from tkinter import ttk
from datetime import date

class ReportsView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.controller = None

        self.create_header()
        self.create_report_treeview()
        self.create_summary_footer()

    def set_controller(self, controller):
        self.controller = controller
        # Conectar el evento de doble clic al método del controlador
        self.tree.bind("<Double-1>", self.controller.show_daily_details)

    def create_header(self):
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        title = ttk.Label(header_frame, text="Reporte de Ventas", font=("Segoe UI", 16, "bold"))
        title.pack(side="left")

    def create_report_treeview(self):
        tree_frame = ttk.Frame(self)
        tree_frame.grid(row=1, column=0, sticky="nsew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_frame, columns=("fecha", "num_ventas", "total"), show="headings")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("num_ventas", text="Nº de Ventas")
        self.tree.heading("total", text="Total Vendido")
        self.tree.column("fecha", anchor=tk.W, width=150)
        self.tree.column("num_ventas", anchor=tk.CENTER, width=120)
        self.tree.column("total", anchor=tk.E, width=150)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def create_summary_footer(self):
        footer_frame = ttk.Frame(self, style="Card.TFrame", padding=10)
        footer_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        self.total_revenue_var = tk.StringVar(value="Ingresos Totales: S/ 0.00")
        ttk.Label(footer_frame, textvariable=self.total_revenue_var, font=("Segoe UI", 12, "bold")).pack(side="right")
    
    def add_daily_summary_to_tree(self, summary_item):
        fecha = summary_item['venta_fecha']
        if isinstance(fecha, date):
            fecha = fecha.strftime('%d/%m/%Y')
        total_formateado = f"S/ {summary_item.get('total_vendido', 0.0):.2f}"
        self.tree.insert("", tk.END, values=(fecha, summary_item.get('numero_ventas', 0), total_formateado))

    def get_selected_date(self):
        """Devuelve la fecha (en formato dd/mm/yyyy) de la fila seleccionada."""
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0], "values")[0]
        return None

    def update_summary_footer(self, total_revenue):
        self.total_revenue_var.set(f"Ingresos Totales: S/ {total_revenue:.2f}")

    def clear_tree(self):
        self.tree.delete(*self.tree.get_children())
