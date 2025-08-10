from tkinter import messagebox
from . import supplier_model as model
from .add_edit_supplier_view import AddEditSupplierView

class SupplierController:
    def __init__(self, main_app_instance):
        self.main_app = main_app_instance
        self.suppliers_view = main_app_instance.views.get('suppliers')
        if self.suppliers_view:
            self.suppliers_view.set_controller(self)
        self.add_edit_window = None

    def load_all_suppliers(self):
        self.search_suppliers() 

    def search_suppliers(self):
        if not self.suppliers_view: return
        search_term = self.suppliers_view.search_var.get()
        suppliers = model.search(search_term)
        self.suppliers_view.clear_tree()
        for supplier in suppliers:
            self.suppliers_view.insert_supplier(supplier)

    def show_add_supplier_window(self):
        if self.add_edit_window and self.add_edit_window.winfo_exists():
            self.add_edit_window.focus()
            return
        self.add_edit_window = AddEditSupplierView(parent=self.main_app, controller=self)
        self.add_edit_window.protocol("WM_DELETE_WINDOW", self.close_add_edit_window)

    def add_supplier(self, data):
        if model.add(data):
            messagebox.showinfo("Éxito", "Proveedor añadido correctamente.", parent=self.main_app)
            self.close_add_edit_window()
            self.load_all_suppliers()
        else:
            messagebox.showerror("Error", "No se pudo añadir el proveedor.", parent=self.add_edit_window)

    def show_edit_supplier_window(self):
        if self.add_edit_window and self.add_edit_window.winfo_exists():
            self.add_edit_window.focus()
            return
            
        supplier_id = self.suppliers_view.get_selected_supplier_id()
        if not supplier_id:
            messagebox.showwarning("Sin Selección", "Por favor, seleccione un proveedor para editar.", parent=self.main_app)
            return
        
        supplier_data = model.get_by_id(supplier_id)
        if not supplier_data:
            messagebox.showerror("Error", "No se encontró el proveedor.", parent=self.main_app)
            return
        
        self.add_edit_window = AddEditSupplierView(parent=self.main_app, controller=self, supplier_data=supplier_data)
        self.add_edit_window.protocol("WM_DELETE_WINDOW", self.close_add_edit_window)

    def update_supplier(self, supplier_id, data):
        if model.update(supplier_id, data):
            messagebox.showinfo("Éxito", "Proveedor actualizado correctamente.", parent=self.main_app)
            self.close_add_edit_window()
            self.load_all_suppliers()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el proveedor.", parent=self.add_edit_window)

    def delete_supplier(self):
        supplier_id = self.suppliers_view.get_selected_supplier_id()
        if not supplier_id:
            messagebox.showwarning("Sin Selección", "Por favor, seleccione un proveedor para eliminar.", parent=self.main_app)
            return

        if messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar a este proveedor?", parent=self.main_app):
            if model.delete(supplier_id):
                messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.", parent=self.main_app)
                self.load_all_suppliers()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el proveedor.", parent=self.main_app)
    
    def close_add_edit_window(self):
        if self.add_edit_window:
            self.add_edit_window.destroy()
        self.add_edit_window = None
