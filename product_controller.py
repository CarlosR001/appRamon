from views.add_product_view import AddProductView
from views.edit_product_view import EditProductView
import product_model as p_model
from tkinter import messagebox

class ProductController:
    def __init__(self, app_view):
        self.app_view = app_view
        self.products_view = app_view.products_view
        self.products_view.set_controller(self)

    def load_products(self, search_term=""):
        """Carga productos (todos o filtrados) y los muestra en la vista."""
        self.products_view.clear_tree()
        product_list = p_model.search_products(search_term)
        for product in product_list:
            self.products_view.add_product_to_tree(product)

    def search_products(self):
        """Obtiene el término de búsqueda de la vista y carga los productos filtrados."""
        search_term = self.products_view.search_var.get()
        self.load_products(search_term)

    def clear_search(self):
        """Limpia la barra de búsqueda y recarga todos los productos."""
        self.products_view.search_var.set("")
        self.load_products()

    def get_selected_product_data(self):
        # ... (código sin cambios)
        selected_item_id = self.products_view.get_selected_item_id()
        if not selected_item_id:
            messagebox.showwarning("Sin Selección", "Por favor, seleccione un producto de la lista.", parent=self.app_view)
            return None
        all_products = p_model.get_all_products()
        selected_product = next((p for p in all_products if p['id'] == selected_item_id), None)
        if not selected_product:
             messagebox.showerror("Error", "No se pudieron encontrar los datos del producto seleccionado.", parent=self.app_view)
             return None
        return selected_product

    def show_add_product_window(self):
        # ... (código sin cambios)
        categories = p_model.get_all_categories()
        if not categories:
            messagebox.showwarning("Sin Categorías", "No se encontraron categorías. Por favor, añada categorías primero.", parent=self.app_view)
            return
        add_view = AddProductView(self.app_view, categories)

    def save_new_product(self, data):
        # ... (código sin cambios)
        product_id = p_model.add_product(data)
        if product_id:
            messagebox.showinfo("Éxito", "Producto añadido correctamente.", parent=self.app_view)
            self.load_products() # Recargar con la nueva data
        else:
            messagebox.showerror("Error de Base de Datos", "No se pudo añadir el producto a la base de datos.", parent=self.app_view)

    def show_edit_product_window(self):
        # ... (código sin cambios)
        selected_product = self.get_selected_product_data()
        if selected_product:
            categories = p_model.get_all_categories()
            edit_view = EditProductView(self.app_view, selected_product, categories)

    def update_existing_product(self, product_id, data):
        # ... (código sin cambios)
        success = p_model.update_product(product_id, data)
        if success:
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.", parent=self.app_view)
            self.load_products() # Recargar con la nueva data
        else:
            messagebox.showerror("Error de Base de Datos", "No se pudo actualizar el producto.", parent=self.app_view)

    def delete_selected_product(self):
        # ... (código sin cambios)
        selected_product = self.get_selected_product_data()
        if selected_product:
            product_name = selected_product.get('nombre', 'el producto')
            answer = messagebox.askyesno("Confirmar Eliminación", 
                                         f"¿Está seguro de que desea eliminar el producto '{product_name}'?\n\nEsta acción no se puede deshacer.",
                                         parent=self.app_view)
            if answer:
                success = p_model.delete_product(selected_product['id'])
                if success:
                    messagebox.showinfo("Éxito", "Producto eliminado correctamente.", parent=self.app_view)
                    self.load_products() # Recargar con la nueva data
                else:
                    messagebox.showerror("Error de Base de Datos", "No se pudo eliminar el producto.", parent=self.app_view)
