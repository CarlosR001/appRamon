import tkinter as tk
from tkinter import messagebox
import product_model as p_model
import sales_model as s_model

class SalesController:
    def __init__(self, app_view):
        self.app_view = app_view
        self.sales_view = None
        self.cart = {}

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
                    product['nombre'], 
                    f"S/ {product['precio_venta']:.2f}", 
                    product['stock'], 
                    product['id']
                ))

    def add_product_to_cart(self, product_id):
        if product_id in self.cart:
            if self.cart[product_id]['qty'] < self.cart[product_id]['data']['stock']:
                self.cart[product_id]['qty'] += 1
            else:
                messagebox.showwarning("Stock Insuficiente", "No hay más stock disponible para este producto.", parent=self.sales_view)
        else:
            all_products = p_model.get_all_products()
            product_data = next((p for p in all_products if p['id'] == product_id), None)
            if product_data:
                if product_data['stock'] > 0:
                    self.cart[product_id] = {'data': product_data, 'qty': 1}
                else:
                    messagebox.showwarning("Sin Stock", "Este producto no tiene stock disponible.", parent=self.sales_view)
        self.update_cart_display()

    def update_cart_display(self):
        if not self.sales_view: return
        tree = self.sales_view.cart_tree
        tree.delete(*tree.get_children())
        
        total_sale = 0
        for product_id, item in self.cart.items():
            qty = item['qty']
            name = item['data']['nombre']
            price = item['data']['precio_venta']
            subtotal = qty * price
            total_sale += subtotal
            
            tree.insert("", tk.END, values=(
                product_id, qty, name, f"S/ {price:.2f}", f"S/ {subtotal:.2f}"
            ))
        
        self.sales_view.total_var.set(f"S/ {total_sale:.2f}")

    def increase_cart_item_qty(self):
        """Aumenta la cantidad del item seleccionado en el carrito."""
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
        """Disminuye la cantidad del item seleccionado en el carrito."""
        selected_id = self.sales_view.get_selected_cart_item_id()
        if not selected_id:
            messagebox.showinfo("Información", "Seleccione un producto del carrito para modificarlo.", parent=self.sales_view)
            return
            
        if selected_id in self.cart:
            self.cart[selected_id]['qty'] -= 1
            if self.cart[selected_id]['qty'] == 0:
                # Si la cantidad llega a cero, eliminamos el producto del carrito
                del self.cart[selected_id]
            self.update_cart_display()

    def remove_cart_item(self):
        """Elimina por completo el item seleccionado del carrito."""
        selected_id = self.sales_view.get_selected_cart_item_id()
        if not selected_id:
            messagebox.showinfo("Información", "Seleccione un producto del carrito para eliminarlo.", parent=self.sales_view)
            return

        if selected_id in self.cart:
            del self.cart[selected_id]
            self.update_cart_display()

    def process_sale(self):
        if not self.cart:
            messagebox.showinfo("Carrito Vacío", "Añada productos para realizar una venta.", parent=self.sales_view)
            return

        total = sum(item['qty'] * item['data']['precio_venta'] for item in self.cart.values())
        
        answer = messagebox.askyesno("Confirmar Venta", f"El total de la venta es S/ {total:.2f}. ¿Desea continuar?", parent=self.sales_view)
        if answer:
            success = s_model.record_sale(self.cart, total)
            if success:
                messagebox.showinfo("Éxito", "Venta registrada correctamente.")
                self.clear_sale(confirm=False)
            else:
                messagebox.showerror("Error", "Ocurrió un error al registrar la venta. La base de datos no ha sido modificada.")

    def clear_sale(self, confirm=True):
        if confirm:
            if not self.cart: return
            answer = messagebox.askyesno("Confirmar Cancelación", "¿Desea cancelar la venta actual?", parent=self.sales_view)
            if not answer:
                return
        
        self.cart.clear()
        self.update_cart_display()
