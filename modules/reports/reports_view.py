import tkinter as tk
from tkinter import ttk
from datetime import date

class ReportsView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.controller = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        title = ttk.Label(header_frame, text="Reportes", font=("Segoe UI", 16, "bold"))
        title.pack(side="left")

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, sticky="nsew")

        self.daily_summary_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.daily_summary_frame, text="Resumen Diario")

        self.product_sales_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.product_sales_frame, text="Ventas por Producto")

        self.profit_summary_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.profit_summary_frame, text="Resumen de Ganancias")

        self.create_daily_summary_widgets()
        self.create_product_sales_widgets()
        self.create_profit_summary_widgets()

    def set_controller(self, controller):
        self.controller = controller
        self.daily_summary_tree.bind("<Double-1>", self.controller.show_daily_details)
        self.notebook.bind("<<NotebookTabChanged>>", self.controller.on_tab_changed)

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

    def create_profit_summary_widgets(self):
        """Crea los widgets para la pestaña de Resumen de Ganancias."""
        self.profit_summary_frame.columnconfigure(0, weight=1)
        
        # --- Creación de variables de texto ---
        self.profit_vars = {
            "revenue": tk.StringVar(value="S/ 0.00"),
            "cogs": tk.StringVar(value="S/ 0.00"),
            "gross_profit": tk.StringVar(value="S/ 0.00"),
            "expenses": tk.StringVar(value="S/ 0.00"),
            "net_profit": tk.StringVar(value="S/ 0.00")
        }
        
        # --- Estructura y visualización ---
        container = ttk.Frame(self.profit_summary_frame, style="Card.TFrame", padding=20)
        container.pack(expand=True)

        # Títulos y valores
        labels = [
            ("(+) Ingresos Totales por Ventas:", self.profit_vars["revenue"]),
            ("(-) Costo de Mercancía Vendida:", self.profit_vars["cogs"]),
            ("(=) Ganancia Bruta:", self.profit_vars["gross_profit"]),
            ("(-) Gastos Operativos:", self.profit_vars["expenses"]),
            ("(=) GANANCIA NETA:", self.profit_vars["net_profit"])
        ]
        
        for i, (text, var) in enumerate(labels):
            is_net_profit = "GANANCIA NETA" in text
            font_size = 16 if is_net_profit else 12
            font_weight = "bold" if is_net_profit else "normal"
            
            label = ttk.Label(container, text=text, font=("Segoe UI", font_size, font_weight))
            label.grid(row=i, column=0, sticky="w", padx=10, pady=8)
            
            value = ttk.Label(container, textvariable=var, font=("Segoe UI", font_size, font_weight))
            value.grid(row=i, column=1, sticky="e", padx=10, pady=8)
        
        # Separador para el resultado final
        ttk.Separator(container, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

    def update_profit_summary(self, summary_data):
        """Actualiza los labels de la pestaña de ganancias con nuevos datos."""
        revenue = summary_data.get('total_revenue', 0.0)
        cogs = summary_data.get('total_cogs', 0.0)
        expenses = summary_data.get('total_expenses', 0.0)
        gross_profit = revenue - cogs
        net_profit = gross_profit - expenses
        
        self.profit_vars["revenue"].set(f"S/ {revenue:.2f}")
        self.profit_vars["cogs"].set(f"S/ {cogs:.2f}")
        self.profit_vars["gross_profit"].set(f"S/ {gross_profit:.2f}")
        self.profit_vars["expenses"].set(f"S/ {expenses:.2f}")
        self.profit_vars["net_profit"].set(f"S/ {net_profit:.2f}")

        # Cambiar color del resultado final
        net_profit_label = self.profit_vars["net_profit"].trace_widget
        if net_profit_label:
             net_profit_label.config(foreground="green" if net_profit >= 0 else "red")
        
        # Hack para obtener el widget real
        for child in self.profit_summary_frame.winfo_children()[0].winfo_children():
            if isinstance(child, ttk.Label) and child.cget("textvariable") == str(self.profit_vars["net_profit"]):
                child.config(foreground="#77dd77" if net_profit >= 0 else "#ff6961") # Verde pastel / Rojo pastel
                break

    def add_daily_summary_to_tree(self, summary_item):
        fecha = summary_item['venta_fecha']
        if isinstance(fecha, date): fecha = fecha.strftime('%d/%m/%Y')
        total_formateado = f"S/ {summary_item.get('total_vendido', 0.0):.2f}"
        self.daily_summary_tree.insert("", tk.END, values=(fecha, summary_item.get('numero_ventas', 0), total_formateado))

    def add_product_sale_to_tree(self, sale_item):
        ingresos_formateado = f"S/ {sale_item.get('total_ingresos', 0.0):.2f}"
        self.product_sales_tree.insert("", tk.END, values=(
            sale_item.get('codigo', 'N/A'), sale_item.get('nombre', ''),
            sale_item.get('total_unidades_vendidas', 0), ingresos_formateado
        ))

    def get_selected_date(self):
        selection = self.daily_summary_tree.selection()
        if selection: return self.daily_summary_tree.item(selection[0], "values")[0]
        return None

    def update_summary_footer(self, total_revenue):
        self.total_revenue_var.set(f"Ingresos Totales: S/ {total_revenue:.2f}")

    def clear_daily_summary_tree(self):
        self.daily_summary_tree.delete(*self.daily_summary_tree.get_children())

    def clear_product_sales_tree(self):
        self.product_sales_tree.delete(*self.product_sales_tree.get_children())
