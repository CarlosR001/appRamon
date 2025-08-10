import tkinter as tk
from tkinter import ttk, messagebox
import product_model
from modules.suppliers import supplier_model
from . import purchase_model as p_model

class PurchaseController:
    def __init__(self, main_app_instance):
        self.main_app = main_app_instance
        self.purchase_view = None
        self.cart = {}
        self.selected_supplier_id = None

    def set_view(self, view):
        self.purchase_view = view
        self.purchase_view.set_controller(self)

    def search_products_for_purchase(self, search_term):
        if not self.purchase_view: return
        tree = self.purchase_view.search_results_tree
        tree.delete(*tree.get_children())
        if search_term:
            results = product_model.search_products(search_term)
            for product in results:
                tree.insert("", tk.END, values=(
                    product.get('nombre', ''),
                    product.get('stock', 0),
                    product.get('id')
                ))

    def add_product_to_cart(self, product_id, cost):
        if product_id in self.cart:
            self.cart[product_id]['qty'] += 1
            self.cart[product_id]['cost'] = cost # Actualizar al último costo ingresado
        else:
            product_data = product_model.get_by_id(product_id)
            if product_data:
                self.cart[product_id] = {'data': product_data, 'qty': 1, 'cost': cost}
        self.update_cart_display()

    def update_cart_display(self):
        if not self.purchase_view: return
        tree = self.purchase_view.cart_tree
        tree.delete(*tree.get_children())
        total = 0
        for product_id, item in self.cart.items():
            qty = item['qty']
            name = item['data'].get('nombre', '')
            cost = item['cost']
            subtotal = qty * cost
            total += subtotal
            tree.insert("", tk.END, values=(
                product_id, qty, name, f"S/ {cost:.2f}", f"S/ {subtotal:.2f}"
            ))
        self.purchase_view.total_var.set(f"S/ {total:.2f}")

    def increase_cart_item_qty(self):
        selected_id = self.purchase_view.get_selected_cart_item_id()
        if selected_id in self.cart:
            self.cart[selected_id]['qty'] += 1
            self.update_cart_display()

    def decrease_cart_item_qty(self):
        selected_id = self.purchase_view.get_selected_cart_item_id()
        if selected_id in self.cart:
            self.cart[selected_id]['qty'] -= 1
            if self.cart[selected_id]['qty'] == 0:
                del self.cart[selected_id]
            self.update_cart_display()

    def remove_cart_item(self):
        selected_id = self.purchase_view.get_selected_cart_item_id()
        if selected_id in self.cart:
            del self.cart[selected_id]
            self.update_cart_display()

    def show_supplier_search_popup(self):
        popup = tk.Toplevel(self.main_app)
        popup.title("Seleccionar Proveedor")
        popup.geometry("450x300")
        popup.transient(self.main_app); popup.grab_set()
        search_frame = ttk.Frame(popup, padding=10); search_frame.pack(fill="x")
        search_frame.columnconfigure(0, weight=1)
        ttk.Label(search_frame, text="Buscar proveedor:").pack(anchor="w")
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var)
        search_entry.pack(fill="x", pady=5)
        results_tree = ttk.Treeview(popup, columns=("id", "nombre"), show="headings", height=5)
        results_tree.heading("id", text="ID"); results_tree.heading("nombre", text="Nombre")
        results_tree.column("id", width=50, anchor="center")
        results_tree.pack(fill="both", expand=True, padx=10, pady=5)
        def update_search(event=None):
            results_tree.delete(*results_tree.get_children())
            for supplier in supplier_model.search(search_var.get()):
                results_tree.insert("", "end", values=(supplier['id'], supplier['nombre']))
        search_entry.bind("<KeyRelease>", update_search)
        def select_supplier():
            selection = results_tree.selection()
            if not selection: return
            s_id, s_name = results_tree.item(selection[0], "values")
            self.selected_supplier_id = int(s_id)
            self.purchase_view.selected_supplier_var.set(f"Proveedor: {s_name}")
            popup.destroy()
        btn_frame = ttk.Frame(popup, padding=10); btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="Seleccionar", command=select_supplier, style="Accent.TButton").pack(side="right")
        ttk.Button(btn_frame, text="Cancelar", command=popup.destroy).pack(side="right", padx=5)
        update_search()

    def process_purchase(self):
        if not self.selected_supplier_id:
            messagebox.showwarning("Proveedor Requerido", "Por favor, seleccione un proveedor.", parent=self.purchase_view)
            return
        if not self.cart:
            messagebox.showinfo("Carrito Vacío", "Añada productos para registrar una compra.", parent=self.purchase_view)
            return
        total = sum(item['qty'] * item['cost'] for item in self.cart.values())
        if messagebox.askyesno("Confirmar Compra", f"El total de la compra es S/ {total:.2f}. ¿Desea continuar?", parent=self.purchase_view):
            if p_model.record_purchase(self.cart, total, self.selected_supplier_id):
                messagebox.showinfo("Éxito", "Compra registrada y stock actualizado.")
                self.clear_purchase(confirm=False)
            else:
                messagebox.showerror("Error", "Ocurrió un error al registrar la compra.")

    def clear_purchase(self, confirm=True):
        if confirm and self.cart:
            if not messagebox.askyesno("Confirmar", "Cancelar la compra actual?", parent=self.purchase_view): return
        self.cart.clear()
        self.selected_supplier_id = None
        self.purchase_view.selected_supplier_var.set("Proveedor: No seleccionado")
        self.update_cart_display()
