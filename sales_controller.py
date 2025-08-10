import tkinter as tk
from tkinter import ttk, messagebox
import product_model as p_model
import sales_model as s_model
from modules.clients import client_model

class SalesController:
    def __init__(self, app_view):
        self.app_view = app_view
        self.sales_view = None
        self.cart = {}
        self.selected_client_id = None # Para guardar el ID del cliente de la venta

    def set_view(self, sales_view):
        self.sales_view = sales_view
        self.sales_view.set_controller(self)

    # --- Métodos de búsqueda de productos (sin cambios) ---
    def search_products_for_sale(self, search_term):
        if not self.sales_view: return
        tree = self.sales_view.search_results_tree
        tree.delete(*tree.get_children())
        if search_term:
            results = p_model.search_products(search_term)
            for product in results:
                tree.insert("", tk.END, values=(
                    product['nombre'], f"S/ {product['precio_venta']:.2f}", product['stock'], product['id']
                ))

    # --- Métodos del carrito (sin cambios) ---
    def add_product_to_cart(self, product_id):
        # ... (lógica existente)
        self.update_cart_display()

    def update_cart_display(self):
        # ... (lógica existente)
        pass

    def increase_cart_item_qty(self):
        # ... (lógica existente)
        pass

    def decrease_cart_item_qty(self):
        # ... (lógica existente)
        pass

    def remove_cart_item(self):
        # ... (lógica existente)
        pass
        
    # --- Lógica de Selección de Cliente (NUEVO) ---
    def show_client_search_popup(self):
        """Crea y muestra una ventana emergente para buscar y seleccionar un cliente."""
        popup = tk.Toplevel(self.app_view)
        popup.title("Seleccionar Cliente")
        popup.geometry("450x300")
        popup.transient(self.app_view)
        popup.grab_set()

        search_frame = ttk.Frame(popup, padding=10)
        search_frame.pack(fill="x")
        search_frame.columnconfigure(0, weight=1)

        ttk.Label(search_frame, text="Buscar cliente por nombre:").pack(anchor="w")
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var)
        search_entry.pack(fill="x", pady=5)
        
        results_tree = ttk.Treeview(popup, columns=("id", "nombre", "telefono"), show="headings", height=5)
        results_tree.heading("id", text="ID")
        results_tree.heading("nombre", text="Nombre")
        results_tree.heading("telefono", text="Teléfono")
        results_tree.column("id", width=50, anchor="center")
        results_tree.pack(fill="both", expand=True, padx=10, pady=5)

        def update_search(event=None):
            term = search_var.get()
            results_tree.delete(*results_tree.get_children())
            clients = client_model.search(term)
            for client in clients:
                results_tree.insert("", "end", values=(client['id'], client['nombre'], client['telefono']))
        
        search_entry.bind("<KeyRelease>", update_search)

        def select_client():
            selection = results_tree.selection()
            if not selection:
                messagebox.showwarning("Sin Selección", "Por favor, seleccione un cliente de la lista.", parent=popup)
                return
            
            client_id, client_name, _ = results_tree.item(selection[0], "values")
            self.selected_client_id = int(client_id)
            self.sales_view.selected_client_var.set(f"Cliente: {client_name}")
            popup.destroy()

        button_frame = ttk.Frame(popup, padding=10)
        button_frame.pack(fill="x")
        ttk.Button(button_frame, text="Seleccionar", command=select_client, style="Accent.TButton").pack(side="right")
        ttk.Button(button_frame, text="Cancelar", command=popup.destroy).pack(side="right", padx=5)

        update_search() # Cargar todos los clientes al inicio

    # --- Lógica de Venta (MODIFICADA) ---
    def process_sale(self):
        if not self.cart:
            messagebox.showinfo("Carrito Vacío", "Añada productos para realizar una venta.", parent=self.sales_view)
            return

        total = sum(item['qty'] * item['data']['precio_venta'] for item in self.cart.values())
        
        client_info = f"para {self.sales_view.selected_client_var.get()}" if self.selected_client_id else "como venta general"
        
        answer = messagebox.askyesno("Confirmar Venta", f"El total de la venta es S/ {total:.2f} {client_info}. ¿Desea continuar?", parent=self.sales_view)
        if answer:
            # Ahora pasamos el ID del cliente (puede ser None) al modelo
            success = s_model.record_sale(self.cart, total, self.selected_client_id)
            if success:
                messagebox.showinfo("Éxito", "Venta registrada correctamente.")
                self.clear_sale(confirm=False)
            else:
                messagebox.showerror("Error", "Ocurrió un error al registrar la venta.")

    def clear_sale(self, confirm=True):
        if confirm:
            if not self.cart: return
            answer = messagebox.askyesno("Confirmar Cancelación", "¿Desea cancelar la venta actual?", parent=self.sales_view)
            if not answer: return
        
        self.cart.clear()
        self.selected_client_id = None # Limpiar cliente
        self.sales_view.selected_client_var.set("Cliente: Público General")
        self.update_cart_display()
