from tkinter import messagebox
from . import service_model
from .add_service_view import AddServiceView
from .update_service_view import UpdateServiceView
from modules.clients import client_model

class ServiceController:
    def __init__(self, main_app_instance):
        self.main_app = main_app_instance
        self.services_view = main_app_instance.views.get('services')
        if self.services_view:
            self.services_view.set_controller(self)
        self.add_window = None
        self.update_window = None

    def load_all_services(self):
        if not self.services_view: return
        self.services_view.clear_tree()
        services = service_model.get_all()
        for service in services:
            self.services_view.insert_service(service)

    def show_add_service_window(self):
        if self.add_window and self.add_window.winfo_exists():
            self.add_window.focus()
            return
        self.add_window = AddServiceView(self.main_app, self)
        self.add_window.protocol("WM_DELETE_WINDOW", self._close_add_window)

    def search_clients_for_service(self, search_term):
        if self.add_window and self.add_window.winfo_exists():
            clients = client_model.search(search_term)
            self.add_window.update_client_list(clients)

    def add_service(self, data):
        if service_model.add(data):
            messagebox.showinfo("Éxito", "Orden de servicio registrada correctamente.", parent=self.add_window)
            self._close_add_window()
            self.load_all_services()
        else:
            messagebox.showerror("Error", "No se pudo registrar la orden de servicio.", parent=self.add_window)

    def show_update_service_window(self):
        """Muestra la ventana para actualizar un servicio existente."""
        if self.update_window and self.update_window.winfo_exists():
            self.update_window.focus()
            return

        service_id = self.services_view.get_selected_service_id()
        if not service_id:
            messagebox.showwarning("Sin Selección", "Por favor, seleccione un servicio de la lista para actualizar.", parent=self.main_app)
            return

        service_data = service_model.get_by_id(service_id)
        if not service_data:
            messagebox.showerror("Error", "No se pudieron obtener los detalles del servicio seleccionado.", parent=self.main_app)
            return
        
        self.update_window = UpdateServiceView(self.main_app, self, service_data)
        self.update_window.protocol("WM_DELETE_WINDOW", self._close_update_window)

    def update_service(self, data):
        """Actualiza la orden de servicio en la base de datos."""
        service_id = data['id']
        new_status = data['status']
        final_cost = data['cost']
        
        if service_model.update(service_id, new_status, final_cost):
            messagebox.showinfo("Éxito", "Orden de servicio actualizada correctamente.", parent=self.update_window)
            self._close_update_window()
            self.load_all_services()
        else:
            messagebox.showerror("Error", "No se pudo actualizar la orden de servicio.", parent=self.update_window)

    def _close_add_window(self):
        if self.add_window:
            self.add_window.destroy()
            self.add_window = None

    def _close_update_window(self):
        if self.update_window:
            self.update_window.destroy()
            self.update_window = None
