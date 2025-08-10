from tkinter import messagebox
from . import expense_model as model

class ExpenseController:
    def __init__(self, main_app_instance):
        self.main_app = main_app_instance
        self.expenses_view = main_app_instance.views.get('expenses')
        if self.expenses_view:
            self.expenses_view.set_controller(self)

    def load_all_expenses(self):
        """Carga todos los gastos del modelo y los muestra en la vista."""
        if not self.expenses_view: return
        self.expenses_view.clear_tree()
        expenses = model.get_all()
        for expense in expenses:
            self.expenses_view.insert_expense(expense)

    def add_expense(self):
        """Añade un nuevo gasto a la base de datos."""
        if not self.expenses_view: return
        
        data = self.expenses_view.get_expense_data()
        if data:
            if model.add(data['description'], data['amount'], data['expense_date']):
                self.expenses_view.show_info("Gasto añadido correctamente.")
                self.expenses_view.clear_form()
                self.load_all_expenses() # Refrescar la lista
            else:
                self.expenses_view.show_error("No se pudo añadir el gasto.")

    def delete_expense(self):
        """Elimina el gasto seleccionado."""
        if not self.expenses_view: return
        
        expense_id = self.expenses_view.get_selected_expense_id()
        if not expense_id:
            messagebox.showwarning("Sin Selección", "Por favor, seleccione un gasto de la lista para eliminar.", parent=self.main_app)
            return

        if messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar este gasto?", parent=self.main_app):
            if model.delete(expense_id):
                messagebox.showinfo("Éxito", "Gasto eliminado correctamente.", parent=self.main_app)
                self.load_all_expenses()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el gasto.", parent=self.main_app)
