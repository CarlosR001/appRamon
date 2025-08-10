from . import category_model as model
from .category_view import CategoriesView

class CategoryController:
    def __init__(self, parent_view):
        self.parent_view = parent_view

    def show_view(self):
        """Crea y muestra la vista de gestión de categorías."""
        self.view = CategoriesView(self.parent_view)
        self.view.set_controller(self)
        self.load_categories()
        self.view.wait_window()

    def load_categories(self):
        """Carga las categorías del modelo y las muestra en la vista."""
        self.view.clear_tree()
        categories = model.get_all()
        for category in categories:
            self.view.insert_category(category)

    def add_category(self):
        """Pide un nombre y añade una nueva categoría."""
        name = self.view.ask_category_name("Añadir Categoría", "Nombre de la nueva categoría:")
        if name:
            if model.add(name):
                self.view.show_info("Categoría añadida con éxito.")
                self.load_categories()
            else:
                self.view.show_error("No se pudo añadir la categoría. ¿Quizás ya existe?")

    def edit_category(self):
        """Edita la categoría seleccionada."""
        category_id = self.view.get_selected_category_id()
        if not category_id:
            self.view.show_error("Por favor, seleccione una categoría para editar.")
            return

        current_name = self.view.get_selected_category_name()
        new_name = self.view.ask_category_name("Editar Categoría", "Nuevo nombre:", initial_value=current_name)
        
        if new_name and new_name != current_name:
            if model.update(category_id, new_name):
                self.view.show_info("Categoría actualizada con éxito.")
                self.load_categories()
            else:
                self.view.show_error("No se pudo actualizar la categoría.")

    def delete_category(self):
        """Elimina la categoría seleccionada tras confirmación."""
        category_id = self.view.get_selected_category_id()
        if not category_id:
            self.view.show_error("Por favor, seleccione una categoría para eliminar.")
            return

        category_name = self.view.get_selected_category_name()
        if self.view.confirm("Confirmar Eliminación", f"¿Está seguro de que desea eliminar la categoría '{category_name}'?"):
            if model.delete(category_id):
                self.view.show_info("Categoría eliminada con éxito.")
                self.load_categories()
            else:
                self.view.show_error("No se pudo eliminar la categoría. Asegúrese de que ningún producto la esté utilizando.")
