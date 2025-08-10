from tkinter import messagebox
from . import service_model
from .add_service_view import AddServiceView
# Importamos el MODELO de clientes, no su controlador.
# Esto mantiene los módulos desacoplados.
from modules.clients import client_model

class ServiceController:
    def __init__(self, main_app_instance):
        self.main_app = main_app_instance
        self.services_view = main_app_instance.views.get('services')
        if self.services_view:
            self.services_view.set_controller(self)
        self.add_window = None

    def load_all_services(self):
        """Carga todas las órdenes de servicio y las muestra en la vista."""
        if not self.services_view: return
        self.services_view.clear_tree()
        services = service_model.get_all()
        for service in services:
            self.services_view.insert_service(service)

    def show_add_service_window(self):
        """Muestra la ventana para registrar una nueva orden de servicio."""
        if self.add_window and self.add_window.winfo_exists():
            self.add_window.focus()
            return
        self.add_window = AddServiceView(self.main_app, self)
        self.add_window.protocol("WM_DELETE_WINDOW", self._close_add_window)

    def search_clients_for_service(self, search_term):
        """Busca clientes y actualiza la lista en la ventana de añadir servicio."""
        if self.add_window and self.add_window.winfo_exists():
            clients = client_model.search(search_term)
            self.add_window.update_client_list(clients)

    def add_service(self, data):
        """Añade la nueva orden de servicio a la base de datos."""
        if service_model.add(data):
            messagebox.showinfo("Éxito", "Orden de servicio registrada correctamente.", parent=self.add_window)
            self._close_add_window()
            self.load_all_services() # Refrescar la lista principal
        else:
            messagebox.showerror("Error", "No se pudo registrar la orden de servicio.", parent=self.add_window)

    def _close_add_window(self):
        """Método privado para cerrar y limpiar la referencia a la ventana emergente."""
        if self.add_window:
            self.add_window.destroy()
            self.add_window = None
