from tkinter import messagebox
from . import client_model as model
from .client_view import ClientsView
from .add_edit_client_view import AddEditClientView

class ClientController:
    def __init__(self, main_app_instance):
        self.main_app = main_app_instance
        self.clients_view = main_app_instance.views.get('clients')
        if self.clients_view:
            self.clients_view.set_controller(self)

    def load_all_clients(self):
        """Carga todos los clientes en la vista principal."""
        self.search_clients("") # Es lo mismo que buscar con un término vacío

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
        add_view = AddEditClientView(parent=self.main_app, controller=self)
        add_view.wait_window()

    def add_client(self, data):
        """Añade un nuevo cliente a la base de datos."""
        if model.add(data):
            messagebox.showinfo("Éxito", "Cliente añadido correctamente.", parent=self.main_app)
            self.load_all_clients()
        else:
            messagebox.showerror("Error", "No se pudo añadir el cliente.", parent=self.main_app)

    def show_edit_client_window(self):
        """Muestra la ventana para editar un cliente existente."""
        client_id = self.clients_view.get_selected_client_id()
        if not client_id:
            messagebox.showwarning("Sin Selección", "Por favor, seleccione un cliente para editar.", parent=self.main_app)
            return
        
        # Obtenemos todos los datos del cliente, no solo los visibles
        client_data = model.search(client_id)[0]
        
        edit_view = AddEditClientView(parent=self.main_app, controller=self, client_data=client_data)
        edit_view.wait_window()

    def update_client(self, client_id, data):
        """Actualiza un cliente en la base de datos."""
        if model.update(client_id, data):
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente.", parent=self.main_app)
            self.load_all_clients()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el cliente.", parent=self.main_app)

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
