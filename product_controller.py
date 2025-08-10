from views.add_product_view import AddProductView
import product_model as p_model
from tkinter import messagebox

class ProductController:
    def __init__(self, app_view):
        self.app_view = app_view # La ventana principal de la aplicación
        self.products_view = app_view.products_view # La pestaña de inventario
        
        # Conectar la vista con este controlador
        self.products_view.set_controller(self)

    def show_add_product_window(self):
        """Muestra la ventana para añadir un nuevo producto."""
        # Obtener categorías de la BD para pasarlas al formulario
        categories = p_model.get_all_categories()
        if not categories:
            messagebox.showwarning("Sin Categorías", "No se encontraron categorías. Por favor, añada categorías primero.")
            # Aquí podría ir la lógica para abrir una ventana de gestión de categorías
            return
            
        # Pasar 'self.app_view' como parent para que la ventana emergente se asocie con la ventana principal
        add_view = AddProductView(self.app_view, categories)
        self.app_view.wait_window(add_view)

    def save_new_product(self, data):
        """Llama al modelo para guardar el nuevo producto y actualiza la vista."""
        product_id = p_model.add_product(data)
        if product_id:
            messagebox.showinfo("Éxito", "Producto añadido correctamente.")
            # Actualizar la tabla de productos para mostrar el nuevo registro
            self.app_view.load_products_data()
        else:
            messagebox.showerror("Error de Base de Datos", "No se pudo añadir el producto a la base de datos.")
