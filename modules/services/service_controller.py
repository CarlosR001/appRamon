from tkinter import messagebox
from . import service_model
from .add_service_view import AddServiceView
from .update_service_view import UpdateServiceView
from modules.clients import client_model
import product_model # Necesitamos el modelo de productos para la búsqueda

class ServiceController:
    def __init__(self, main_app_instance):
        self.main_app = main_app_instance
        self.services_view = main_app_instance.views.get('services')
        if self.services_view:
            self.services_view.set_controller(self)
        self.add_window = None
        self.update_window = None
        self.current_service_id = None

    def load_all_services(self):
        if not self.services_view: return
        self.services_view.clear_tree()
        services = service_model.get_all()
        for service in services:
            self.services_view.insert_service(service)

    def show_add_service_window(self):
        if self.add_window and self.add_window.winfo_exists():
            self.add_window.focus(); return
        self.add_window = AddServiceView(self.main_app, self)
        self.add_window.protocol("WM_DELETE_WINDOW", self._close_add_window)

    def add_service(self, data):
        if service_model.add(data):
            messagebox.showinfo("Éxito", "Orden de servicio registrada.", parent=self.add_window)
            self._close_add_window()
            self.load_all_services()
        else:
            messagebox.showerror("Error", "No se pudo registrar la orden.", parent=self.add_window)

    def show_update_service_window(self):
        """Muestra la ventana para actualizar un servicio existente."""
        if self.update_window and self.update_window.winfo_exists():
            self.update_window.focus(); return
        
        self.current_service_id = self.services_view.get_selected_service_id()
        if not self.current_service_id:
            messagebox.showwarning("Sin Selección", "Seleccione un servicio para actualizar.", parent=self.main_app)
            return

        service_data = service_model.get_by_id(self.current_service_id)
        if not service_data:
            messagebox.showerror("Error", "No se encontraron los detalles del servicio.", parent=self.main_app)
            return
        
        self.update_window = UpdateServiceView(self.main_app, self, service_data)
        self.update_window.protocol("WM_DELETE_WINDOW", self._close_update_window)
        self.refresh_service_details()

    def refresh_service_details(self):
        """Recarga los items y el costo total en la ventana de actualización."""
        if not (self.update_window and self.update_window.winfo_exists()): return
        
        service_data = service_model.get_by_id(self.current_service_id)
        service_cost = service_data.get('costo_servicio', 0.0)
        
        items = service_model.get_service_items(self.current_service_id)
        self.update_window.update_service_items_list(items)
        
        items_cost = sum(i['cantidad'] * i['precio_venta_unitario'] for i in items)
        total_cost = service_cost + items_cost
        self.update_window.update_total_cost(total_cost)

    def search_products_for_service(self, search_term):
        """Busca productos y actualiza la lista en la ventana de actualización de servicio."""
        if self.update_window and self.update_window.winfo_exists():
            products = product_model.search_products(search_term)
            self.update_window.update_search_results(products)
    
    def search_clients_for_service(self, search_term):
        if self.add_window and self.add_window.winfo_exists():
            clients = client_model.search(search_term)
            self.add_window.update_client_list(clients)

    def add_item_to_service(self, product_id, quantity):
        product = product_model.get_by_id(product_id)
        if service_model.add_item_to_service(self.current_service_id, product, quantity):
            self.refresh_service_details()
        else:
            messagebox.showerror("Error", "No se pudo añadir el repuesto. Verifique el stock.", parent=self.update_window)

    def remove_item_from_service(self, detail_id):
        items = service_model.get_service_items(self.current_service_id)
        # BUG FIX: detail_id is a string from the treeview, needs to be int for comparison
        item_to_remove = next((i for i in items if i['id'] == int(detail_id)), None)
        if not item_to_remove: return

        product_id = item_to_remove['id_producto']
        quantity = item_to_remove['cantidad']
        
        if service_model.remove_item_from_service(detail_id, product_id, quantity):
            self.refresh_service_details()
        else:
            messagebox.showerror("Error", "No se pudo quitar el repuesto.", parent=self.update_window)

    def update_service_status_and_cost(self, new_status, service_cost):
        if service_model.update_status_and_cost(self.current_service_id, new_status, service_cost):
            messagebox.showinfo("Éxito", "Orden actualizada.", parent=self.update_window)
            self._close_update_window()
            self.load_all_services()
        else:
            messagebox.showerror("Error", "No se pudo actualizar la orden.", parent=self.update_window)

    def _close_add_window(self):
        if self.add_window: self.add_window.destroy(); self.add_window = None
    
    def _close_update_window(self):
        if self.update_window: self.update_window.destroy(); self.update_window = None

    def show_service_details_popup(self):
        """Muestra una ventana emergente con todos los detalles del servicio."""
        service_id = self.services_view.get_selected_service_id()
        if not service_id:
            messagebox.showwarning("Sin Selección", "Seleccione un servicio de la lista para ver sus detalles.", parent=self.main_app)
            return

        # Reutilizamos la lógica de la ventana de actualización, pero en modo "solo lectura"
        # En una futura mejora, se podría crear una vista de detalles específica.
        self.show_update_service_window()
