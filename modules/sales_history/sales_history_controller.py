from tkinter import messagebox
from . import sales_history_model as model
import sales_model # Para obtener los detalles de la venta a reimprimir
from modules.printing import pdf_generator

class SalesHistoryController:
    def __init__(self, main_app_instance):
        self.main_app = main_app_instance
        self.history_view = main_app_instance.views.get('sales_history')
        if self.history_view:
            self.history_view.set_controller(self)
            
    def load_sales_history(self):
        """Carga el historial de ventas, aplicando el filtro de fecha si existe."""
        if not self.history_view: return
        
        start_date, end_date = None, None
        try:
            # Esta sección se ejecuta solo si tkcalendar está disponible
            start_date = self.history_view.start_date_entry.get_date()
            end_date = self.history_view.end_date_entry.get_date()
        except AttributeError:
            # Si tkcalendar no está, se cargarán todas las ventas
            pass
            
        self.history_view.clear_tree()
        sales = model.search_sales(start_date, end_date)
        for sale in sales:
            self.history_view.insert_sale(sale)

    def reprint_receipt(self):
        """Obtiene los datos de la venta seleccionada y genera el recibo."""
        sale_id = self.history_view.get_selected_sale_id()
        if not sale_id:
            messagebox.showwarning("Sin Selección", "Por favor, seleccione una venta para reimprimir.", parent=self.main_app)
            return

        receipt_data = sales_model.get_sale_details_for_receipt(sale_id)
        if receipt_data:
            # Preguntar el formato
            # En una futura mejora, podríamos tener un diálogo más complejo
            # Por ahora, generaremos el formato de ticket por defecto
            pdf_generator.generate_receipt(receipt_data, "ticket")
            messagebox.showinfo("Recibo Generado", f"Se ha generado el recibo para la venta #{sale_id}.", parent=self.main_app)
        else:
            messagebox.showerror("Error", "No se pudieron obtener los detalles de la venta seleccionada.", parent=self.main_app)

    def void_sale(self):
        """Anula la venta seleccionada tras confirmación."""
        sale_id = self.history_view.get_selected_sale_id()
        if not sale_id:
            messagebox.showwarning("Sin Selección", "Por favor, seleccione una venta para anular.", parent=self.main_app)
            return

        # Doble confirmación para una acción destructiva
        answer = messagebox.askyesno("Confirmar Anulación", 
                                     f"¿Está seguro de que desea anular la venta #{sale_id}?\n\nEsta acción no se puede deshacer y el stock de los productos será restaurado.", 
                                     parent=self.main_app)
        
        if answer:
            if model.void_sale(sale_id):
                messagebox.showinfo("Éxito", f"La venta #{sale_id} ha sido anulada correctamente.", parent=self.main_app)
                self.load_sales_history() # Recargar la lista para ver el cambio de estado
            else:
                messagebox.showerror("Error", "No se pudo anular la venta.", parent=self.main_app)
