import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class UpdateServiceView(tk.Toplevel):
    def __init__(self, parent, controller, service_data):
        super().__init__(parent)
        self.controller = controller
        self.service_data = service_data

        self.title(f"Gestionar Servicio #{service_data.get('id')}")
        self.geometry("850x650")
        self.resizable(True, True)
        self.grab_set()

        # --- Layout Principal ---
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(expand=True, fill="both")
        main_frame.rowconfigure(2, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # --- 1. Panel de Información y Actualización de Estado ---
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        top_frame.columnconfigure(1, weight=1)

        # -- Detalles de la Orden --
        info_frame = ttk.LabelFrame(top_frame, text="Detalles de la Orden", padding=10)
        info_frame.grid(row=0, column=0, sticky="nsw", padx=(0,10))
        info_frame.columnconfigure(1, weight=1)
        
        info_labels = { "Cliente:": service_data.get('nombre_cliente', 'N/A'),
                        "Teléfono:": service_data.get('telefono_cliente', 'N/A'),
                        "Equipo:": service_data.get('descripcion_equipo', ''),
                        "Fecha Recepción:": service_data.get('fecha_recepcion', '').strftime('%d/%m/%Y %H:%M') }
        for i, (label, value) in enumerate(info_labels.items()):
            ttk.Label(info_frame, text=label, font=("Segoe UI", 10, "bold")).grid(row=i, column=0, sticky="nw", pady=2)
            ttk.Label(info_frame, text=value, wraplength=250).grid(row=i, column=1, sticky="w", padx=5, pady=2)
        
        # -- Actualizar Orden --
        update_frame = ttk.LabelFrame(top_frame, text="Actualizar Orden", padding=10)
        update_frame.grid(row=0, column=1, sticky="nsew")
        update_frame.columnconfigure(1, weight=1)
        ttk.Label(update_frame, text="Estado:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.status_var = tk.StringVar(value=service_data.get('estado', 'Recibido'))
        status_options = ['Recibido', 'En Diagnostico', 'Esperando Piezas', 'En Reparacion', 'Listo', 'Entregado']
        ttk.Combobox(update_frame, textvariable=self.status_var, values=status_options, state="readonly").grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(update_frame, text="Costo Mano de Obra (S/):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.service_cost_var = tk.DoubleVar(value=service_data.get('costo_servicio', 0.0))
        ttk.Entry(update_frame, textvariable=self.service_cost_var).grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # --- 2. Panel para Añadir Repuestos ---
        add_item_frame = ttk.LabelFrame(main_frame, text="Añadir Repuestos/Productos al Servicio", padding=10)
        add_item_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        add_item_frame.columnconfigure(1, weight=1)
        ttk.Label(add_item_frame, text="Buscar Producto:").grid(row=0, column=0, padx=5, pady=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(add_item_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        search_entry.bind("<KeyRelease>", lambda e: self.controller.search_products_for_service(self.search_var.get()))
        self.search_results_tree = ttk.Treeview(add_item_frame, columns=("id", "nombre", "stock", "precio"), show="headings", height=3, displaycolumns=("nombre", "stock", "precio"))
        self.search_results_tree.heading("nombre", text="Producto"); self.search_results_tree.heading("stock", text="Stock"); self.search_results_tree.heading("precio", text="Precio Venta")
        self.search_results_tree.column("stock", width=60, anchor="c"); self.search_results_tree.column("precio", width=90, anchor="e")
        self.search_results_tree.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        self.search_results_tree.bind("<Double-1>", self.on_product_select)

        # --- 3. Panel de Repuestos Añadidos y Totales ---
        items_frame = ttk.LabelFrame(main_frame, text="Repuestos Añadidos", padding=10)
        items_frame.grid(row=2, column=0, sticky="nsew")
        items_frame.columnconfigure(0, weight=1); items_frame.rowconfigure(0, weight=1)
        self.service_items_tree = ttk.Treeview(items_frame, columns=("detail_id", "prod_id", "qty", "nombre", "precio", "subtotal"), show="headings", displaycolumns=("qty", "nombre", "precio", "subtotal"))
        self.service_items_tree.heading("qty", text="Cant."); self.service_items_tree.heading("nombre", text="Producto"); self.service_items_tree.heading("precio", text="P. Unit."); self.service_items_tree.heading("subtotal", text="Subtotal")
        self.service_items_tree.column("qty", width=40, anchor="c"); self.service_items_tree.column("precio", width=90, anchor="e"); self.service_items_tree.column("subtotal", width=90, anchor="e")
        self.service_items_tree.grid(row=0, column=0, sticky="nsew")
        self.remove_item_button = ttk.Button(items_frame, text="Quitar Repuesto Seleccionado", command=self.on_remove_item)
        self.remove_item_button.grid(row=1, column=0, sticky="e", pady=5)
        total_frame = ttk.Frame(items_frame); total_frame.grid(row=2, column=0, sticky="e", pady=10)
        self.total_cost_var = tk.StringVar(value="Costo Total: S/ 0.00")
        ttk.Label(total_frame, textvariable=self.total_cost_var, font=("Segoe UI", 12, "bold")).pack()
        
        # --- 4. Botón Final de Guardado ---
        save_button = ttk.Button(main_frame, text="Guardar Cambios en la Orden", style="Accent.TButton", command=self.save_all_changes)
        save_button.grid(row=3, column=0, sticky="e", pady=(15,0))

    def on_product_select(self, event):
        selection = self.search_results_tree.selection()
        if not selection: return
        item = self.search_results_tree.item(selection[0], "values")
        product_id = item[0]
        product_stock = int(item[2])
        
        if product_stock <= 0:
            messagebox.showwarning("Sin Stock", "Este producto no tiene stock disponible.", parent=self)
            return

        qty = simpledialog.askinteger("Cantidad", "Ingrese la cantidad a utilizar:", parent=self, minvalue=1, maxvalue=product_stock)
        if qty:
            self.controller.add_item_to_service(product_id, qty)

    def on_remove_item(self):
        selection = self.service_items_tree.selection()
        if not selection:
            messagebox.showwarning("Sin Selección", "Seleccione un repuesto de la lista para quitarlo.", parent=self)
            return
        item_values = self.service_items_tree.item(selection[0], "values")
        detail_id = item_values[0]
        self.controller.remove_item_from_service(detail_id)

    def save_all_changes(self):
        try:
            new_status = self.status_var.get()
            service_cost = self.service_cost_var.get()
            if not new_status:
                messagebox.showwarning("Estado no seleccionado", "Por favor, seleccione un estado.", parent=self)
                return
            if service_cost < 0:
                messagebox.showwarning("Costo Inválido", "El costo no puede ser negativo.", parent=self)
                return
            
            self.controller.update_service_status_and_cost(new_status, service_cost)
        except tk.TclError:
            messagebox.showerror("Dato Inválido", "Por favor, ingrese un costo numérico válido.", parent=self)

    def update_search_results(self, products):
        self.search_results_tree.delete(*self.search_results_tree.get_children())
        for p in products:
            self.search_results_tree.insert("", "end", values=(p['id'], p['nombre'], p['stock'], f"S/ {p['precio_venta']:.2f}"))

    def update_service_items_list(self, items):
        self.service_items_tree.delete(*self.service_items_tree.get_children())
        for i in items:
            subtotal = i['cantidad'] * i['precio_venta_unitario']
            self.service_items_tree.insert("", "end", values=(i['id'], i['id_producto'], i['cantidad'], i['nombre'], f"S/ {i['precio_venta_unitario']:.2f}", f"S/ {subtotal:.2f}"))
    
    def update_total_cost(self, total_cost):
        self.total_cost_var.set(f"Costo Total (M. Obra + Repuestos): S/ {total_cost:.2f}")

