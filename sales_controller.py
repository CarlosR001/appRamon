import tkinter as tk
from tkinter import messagebox
import product_model as p_model

class SalesController:
    def __init__(self, app_view):
        self.app_view = app_view
        self.sales_view = None  # Se asignará cuando se cree la vista
        self.cart = {} # Diccionario para el carrito: {product_id: {data}, qty: X}

    def set_view(self, sales_view):
        """Asigna la vista de ventas a este controlador."""
        self.sales_view = sales_view
        self.sales_view.set_controller(self)

    def search_products_for_sale(self, search_term):
        """Busca productos y los muestra en la tabla de resultados del TPV."""
        if self.sales_view:
            # Limpiar resultados anteriores
            for i in self.sales_view.search_results_tree.get_children():
                self.sales_view.search_results_tree.delete(i)
            
            # Realizar la búsqueda si el término no está vacío
            if search_term:
                results = p_model.search_products(search_term)
                for product in results:
                    # Guardamos el ID en una columna "oculta" que no se muestra
                    self.sales_view.search_results_tree.insert(
                        "", tk.END, 
                        values=(product['nombre'], f"S/ {product['precio_venta']:.2f}", product['stock'], product['id'])
                    )

    def add_product_to_cart(self, product_id):
        """Añade un producto al carrito o incrementa su cantidad."""
        if product_id in self.cart:
            # Si el producto ya está, solo incrementamos la cantidad
            # Comprobando si hay stock suficiente
            if self.cart[product_id]['qty'] < self.cart[product_id]['data']['stock']:
                self.cart[product_id]['qty'] += 1
            else:
                messagebox.showwarning("Stock Insuficiente", "No hay más stock disponible para este producto.", parent=self.sales_view)
        else:
            # Si es un producto nuevo, lo buscamos en la BD
            all_products = p_model.get_all_products()
            product_data = next((p for p in all_products if p['id'] == product_id), None)
            if product_data:
                if product_data['stock'] > 0:
                    self.cart[product_id] = {'data': product_data, 'qty': 1}
                else:
                    messagebox.showwarning("Sin Stock", "Este producto no tiene stock disponible.", parent=self.sales_view)
        
        self.update_cart_display()

    def update_cart_display(self):
        """Refresca la tabla del carrito y el total de la venta."""
        if not self.sales_view:
            return

        # Limpiar carrito
        for i in self.sales_view.cart_tree.get_children():
            self.sales_view.cart_tree.delete(i)
        
        total_sale = 0
        # Añadir productos del carrito a la tabla
        for product_id, item in self.cart.items():
            qty = item['qty']
            name = item['data']['nombre']
            price = item['data']['precio_venta']
            subtotal = qty * price
            total_sale += subtotal
            
            self.sales_view.cart_tree.insert(
                "", tk.END, 
                values=(qty, name, f"S/ {price:.2f}", f"S/ {subtotal:.2f}")
            )
        
        # Actualizar el label del total
        self.sales_view.total_var.set(f"S/ {total_sale:.2f}")

    def process_sale(self):
        """Procesa la venta final (a implementar)."""
        if not self.cart:
            messagebox.showinfo("Carrito Vacío", "Añada productos al carrito para poder realizar una venta.", parent=self.sales_view)
            return
        
        # Aquí irá la lógica para:
        # 1. Mostrar una ventana de confirmación con el total.
        # 2. Guardar la venta y sus detalles en la BD.
        # 3. Actualizar el stock de cada producto en la BD.
        # 4. Limpiar el carrito.
        messagebox.showinfo("Función en Desarrollo", "La finalización de la venta aún no está implementada.", parent=self.sales_view)

    def clear_sale(self):
        """Cancela la venta actual, limpiando el carrito."""
        if self.cart:
            answer = messagebox.askyesno("Confirmar Cancelación", "¿Está seguro de que desea cancelar la venta actual? Se perderán todos los productos del carrito.", parent=self.sales_view)
            if answer:
                self.cart.clear()
                self.update_cart_display()
