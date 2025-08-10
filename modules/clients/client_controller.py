from tkinter import messagebox
from . import client_model as model
from .add_edit_client_view import AddEditClientView

class ClientController:
    def __init__(self, main_app_instance):
        self.main_app = main_app_instance
        self.clients_view = main_app_instance.views.get('clients')
        if self.clients_view:
            self.clients_view.set_controller(self)
        self.add_edit_window = None # Para mantener una referencia a la ventana emergente

    def load_all_clients(self):
        """Carga todos los clientes en la vista principal."""
        self.search_clients() 

    def search_clients(self):
        """Busca clientes según el término en la vista y los muestra."""
        if not self.clients_view: return
        search_term = self.clients_view.search_var.get()
        clients = model.search(search_term)
        self.clients_view.clear_tree()
        for client in clients:
            self.clients_view.insert_client(client)

    def show_add_client_window(self):
        """Muestra la ventana para añadir un nuevo cliente."""
        if self.add_edit_window is not None and self.add_edit_window.winfo_exists():
            self.add_edit_window.focus()
            return
        self.add_edit_window = AddEditClientView(parent=self.main_app, controller=self)
        self.add_edit_window.protocol("WM_DELETE_WINDOW", self.close_add_edit_window)

    def add_client(self, data):
        """Añade un nuevo cliente a la base de datos."""
        if model.add(data):
            messagebox.showinfo("Éxito", "Cliente añadido correctamente.", parent=self.main_app)
            self.close_add_edit_window()
            self.load_all_clients()
        else:
            messagebox.showerror("Error", "No se pudo añadir el cliente.", parent=self.add_edit_window)

    def show_edit_client_window(self):
        """Muestra la ventana para editar un cliente existente."""
        if self.add_edit_window is not None and self.add_edit_window.winfo_exists():
            self.add_edit_window.focus()
            return
            
        client_id = self.clients_view.get_selected_client_id()
        if not client_id:
            messagebox.showwarning("Sin Selección", "Por favor, seleccione un cliente para editar.", parent=self.main_app)
            return
        
        client_data = model.get_by_id(client_id)
        if not client_data:
            messagebox.showerror("Error", "No se encontró el cliente.", parent=self.main_app)
            return
        
        self.add_edit_window = AddEditClientView(parent=self.main_app, controller=self, client_data=client_data)
        self.add_edit_window.protocol("WM_DELETE_WINDOW", self.close_add_edit_window)

    def update_client(self, client_id, data):
        """Actualiza un cliente en la base de datos."""
        if model.update(client_id, data):
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente.", parent=self.main_app)
            self.close_add_edit_window()
            self.load_all_clients()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el cliente.", parent=self.add_edit_window)

    def delete_client(self):
        """Elimina el cliente seleccionado."""
        client_id = self.clients_view.get_selected_client_id()
        if not client_id:
            messagebox.showwarning("Sin Selección", "Por favor, seleccione un cliente para eliminar.", parent=self.main_app)
            return

        if messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar a este cliente?", parent=self.main_app):
            if model.delete(client_id):
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.", parent=self.main_app)
                self.load_all_clients()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente. Verifique si tiene ventas o servicios asociados.", parent=self.main_app)
    
    def close_add_edit_window(self):
        if self.add_edit_window:
            self.add_edit_window.destroy()
        self.add_edit_window = None
