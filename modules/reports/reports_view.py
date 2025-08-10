import tkinter as tk
from tkinter import ttk
from datetime import date

class ReportsView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.controller = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # --- Header ---
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        title = ttk.Label(header_frame, text="Reportes", font=("Segoe UI", 16, "bold"))
        title.pack(side="left")

        # --- Notebook for Tabs ---
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, sticky="nsew")

        # --- Tab 1: Daily Summary ---
        self.daily_summary_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.daily_summary_frame, text="Resumen Diario de Ventas")
        self.create_daily_summary_widgets()

        # --- Tab 2: Sales by Product ---
        self.product_sales_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.product_sales_frame, text="Ventas por Producto")
        self.create_product_sales_widgets()

    def set_controller(self, controller):
        self.controller = controller
        self.daily_summary_tree.bind("<Double-1>", self.controller.show_daily_details)
        self.notebook.bind("<<NotebookTabChanged>>", self.controller.on_tab_changed)

    # --- Widgets for Daily Summary Tab ---
    def create_daily_summary_widgets(self):
        self.daily_summary_frame.columnconfigure(0, weight=1)
        self.daily_summary_frame.rowconfigure(0, weight=1)

        tree_frame = ttk.Frame(self.daily_summary_frame)
        tree_frame.grid(row=0, column=0, sticky="nsew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        self.daily_summary_tree = ttk.Treeview(tree_frame, columns=("fecha", "num_ventas", "total"), show="headings")
        self.daily_summary_tree.heading("fecha", text="Fecha")
        self.daily_summary_tree.heading("num_ventas", text="Nº de Ventas")
        self.daily_summary_tree.heading("total", text="Total Vendido")
        self.daily_summary_tree.column("fecha", anchor=tk.W, width=150)
        self.daily_summary_tree.column("num_ventas", anchor=tk.CENTER, width=120)
        self.daily_summary_tree.column("total", anchor=tk.E, width=150)
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.daily_summary_tree.yview)
        self.daily_summary_tree.configure(yscroll=scrollbar.set)
        self.daily_summary_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        footer_frame = ttk.Frame(self.daily_summary_frame, style="Card.TFrame", padding=10)
        footer_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        self.total_revenue_var = tk.StringVar(value="Ingresos Totales: S/ 0.00")
        ttk.Label(footer_frame, textvariable=self.total_revenue_var, font=("Segoe UI", 12, "bold")).pack(side="right")

    # --- Widgets for Product Sales Tab ---
    def create_product_sales_widgets(self):
        self.product_sales_frame.columnconfigure(0, weight=1)
        self.product_sales_frame.rowconfigure(0, weight=1)

        self.product_sales_tree = ttk.Treeview(self.product_sales_frame, columns=("codigo", "nombre", "unidades", "ingresos"), show="headings")
        self.product_sales_tree.heading("codigo", text="Código")
        self.product_sales_tree.heading("nombre", text="Producto")
        self.product_sales_tree.heading("unidades", text="Unidades Vendidas")
        self.product_sales_tree.heading("ingresos", text="Total Ingresos")
        self.product_sales_tree.column("codigo", anchor=tk.W, width=120)
        self.product_sales_tree.column("nombre", anchor=tk.W, width=300)
        self.product_sales_tree.column("unidades", anchor=tk.CENTER, width=120)
        self.product_sales_tree.column("ingresos", anchor=tk.E, width=150)
        
        scrollbar = ttk.Scrollbar(self.product_sales_frame, orient=tk.VERTICAL, command=self.product_sales_tree.yview)
        self.product_sales_tree.configure(yscroll=scrollbar.set)
        self.product_sales_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # --- Methods to interact with the widgets ---
    def add_daily_summary_to_tree(self, summary_item):
        fecha = summary_item['venta_fecha']
        if isinstance(fecha, date):
            fecha = fecha.strftime('%d/%m/%Y')
        total_formateado = f"S/ {summary_item.get('total_vendido', 0.0):.2f}"
        self.daily_summary_tree.insert("", tk.END, values=(fecha, summary_item.get('numero_ventas', 0), total_formateado))

    def add_product_sale_to_tree(self, sale_item):
        ingresos_formateado = f"S/ {sale_item.get('total_ingresos', 0.0):.2f}"
        self.product_sales_tree.insert("", tk.END, values=(
            sale_item.get('codigo', 'N/A'),
            sale_item.get('nombre', ''),
            sale_item.get('total_unidades_vendidas', 0),
            ingresos_formateado
        ))

    def get_selected_date(self):
        selection = self.daily_summary_tree.selection()
        if selection:
            return self.daily_summary_tree.item(selection[0], "values")[0]
        return None

    def update_summary_footer(self, total_revenue):
        self.total_revenue_var.set(f"Ingresos Totales: S/ {total_revenue:.2f}")

    def clear_daily_summary_tree(self):
        self.daily_summary_tree.delete(*self.daily_summary_tree.get_children())

    def clear_product_sales_tree(self):
        self.product_sales_tree.delete(*self.product_sales_tree.get_children())
