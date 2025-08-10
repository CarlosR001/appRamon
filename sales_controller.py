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
        self.selected_client_id = None

    def set_view(self, sales_view):
        self.sales_view = sales_view
        self.sales_view.set_controller(self)

    def search_products_for_sale(self, search_term):
        if not self.sales_view: return
        tree = self.sales_view.search_results_tree
        tree.delete(*tree.get_children())
        if search_term:
            results = p_model.search_products(search_term)
            for product in results:
                tree.insert("", tk.END, values=(
                    product.get('nombre', ''),
                    f"S/ {product.get('precio_venta', 0.0):.2f}",
                    product.get('stock', 0),
                    product.get('id')
                ))

    def add_product_to_cart(self, product_id):
        """Añade un producto al carrito o incrementa su cantidad."""
        if product_id in self.cart:
            # Si el producto ya está, solo incrementamos la cantidad
            if self.cart[product_id]['qty'] < self.cart[product_id]['data']['stock']:
                self.cart[product_id]['qty'] += 1
            else:
                messagebox.showwarning("Stock Insuficiente", "No hay más stock disponible para este producto.", parent=self.sales_view)
        else:
            # CORRECCIÓN: Usar el modelo de productos para obtener datos frescos
            product_data = p_model.search_products(str(product_id))
            if product_data:
                product_data = product_data[0] # search_products devuelve una lista
                if product_data['stock'] > 0:
                    self.cart[product_id] = {'data': product_data, 'qty': 1}
                else:
                    messagebox.showwarning("Sin Stock", "Este producto no tiene stock disponible.", parent=self.sales_view)
            else:
                messagebox.showerror("Error", f"No se pudo encontrar el producto con ID {product_id}.", parent=self.sales_view)
        
        self.update_cart_display()

    def update_cart_display(self):
        """Refresca la tabla del carrito y el total de la venta."""
        if not self.sales_view: return
        tree = self.sales_view.cart_tree
        tree.delete(*tree.get_children())
        
        total_sale = 0
        for product_id, item in self.cart.items():
            qty = item['qty']
            name = item['data'].get('nombre', '')
            price = item['data'].get('precio_venta', 0.0)
            subtotal = qty * price
            total_sale += subtotal
            
            tree.insert("", tk.END, values=(
                product_id, qty, name, f"S/ {price:.2f}", f"S/ {subtotal:.2f}"
            ))
        
        self.sales_view.total_var.set(f"S/ {total_sale:.2f}")

    def increase_cart_item_qty(self):
        selected_id = self.sales_view.get_selected_cart_item_id()
        if not selected_id:
            messagebox.showinfo("Información", "Seleccione un producto del carrito para modificarlo.", parent=self.sales_view)
            return
        
        if selected_id in self.cart:
            if self.cart[selected_id]['qty'] < self.cart[selected_id]['data']['stock']:
                self.cart[selected_id]['qty'] += 1
                self.update_cart_display()
            else:
                messagebox.showwarning("Stock Insuficiente", "No hay más stock disponible.", parent=self.sales_view)

    def decrease_cart_item_qty(self):
        selected_id = self.sales_view.get_selected_cart_item_id()
        if not selected_id:
            messagebox.showinfo("Información", "Seleccione un producto del carrito para modificarlo.", parent=self.sales_view)
            return
            
        if selected_id in self.cart:
            self.cart[selected_id]['qty'] -= 1
            if self.cart[selected_id]['qty'] == 0:
                del self.cart[selected_id]
            self.update_cart_display()

    def remove_cart_item(self):
        selected_id = self.sales_view.get_selected_cart_item_id()
        if not selected_id:
            messagebox.showinfo("Información", "Seleccione un producto del carrito para eliminarlo.", parent=self.sales_view)
            return

        if selected_id in self.cart:
            del self.cart[selected_id]
            self.update_cart_display()

    def show_client_search_popup(self):
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

        update_search()

    def process_sale(self):
        if not self.cart:
            messagebox.showinfo("Carrito Vacío", "Añada productos para realizar una venta.", parent=self.sales_view)
            return

        total = sum(item['qty'] * item['data']['precio_venta'] for item in self.cart.values())
        
        client_info = f"para {self.sales_view.selected_client_var.get()}" if self.selected_client_id else "como venta general"
        
        answer = messagebox.askyesno("Confirmar Venta", f"El total de la venta es S/ {total:.2f} {client_info}. ¿Desea continuar?", parent=self.sales_view)
        if answer:
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
        self.selected_client_id = None
        self.sales_view.selected_client_var.set("Cliente: Público General")
        self.update_cart_display()
