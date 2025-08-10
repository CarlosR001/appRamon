from . import reports_model as model
from .daily_detail_view import DailyDetailView
from datetime import datetime

class ReportsController:
    def __init__(self, app_view):
        self.app_view = app_view
        self.reports_view = None
        self.detail_window = None

    def set_view(self, view):
        """Asigna la vista a este controlador."""
        self.reports_view = view
        self.reports_view.set_controller(self)

    def load_data(self):
        """
        Carga los datos desde el modelo, los procesa y los envía a la vista
        para ser mostrados.
        """
        if not self.reports_view:
            return

        self.reports_view.clear_tree()

        daily_summary = model.get_daily_sales_summary()

        total_revenue = 0
        for item in daily_summary:
            self.reports_view.add_daily_summary_to_tree(item)
            total_revenue += item.get('total_vendido', 0)
            
        self.reports_view.update_summary_footer(total_revenue)

    def show_daily_details(self, event=None):
        """
        Manejador para el evento de doble clic. Muestra los detalles de venta
        para la fecha seleccionada.
        """
        if not self.reports_view: return

        selected_date_str = self.reports_view.get_selected_date()
        if not selected_date_str:
            return

        # Convertir la fecha de string (dd/mm/yyyy) a un objeto date
        try:
            sale_date = datetime.strptime(selected_date_str, '%d/%m/%Y').date()
        except ValueError:
            print(f"Error al convertir la fecha: {selected_date_str}")
            return
            
        # Evitar abrir múltiples ventanas
        if self.detail_window and self.detail_window.winfo_exists():
            self.detail_window.focus()
            return
            
        # Obtener los datos y mostrar la ventana de detalles
        sales_data = model.get_sales_details_for_date(sale_date)
        self.detail_window = DailyDetailView(self.app_view, sales_data, sale_date)
        self.detail_window.protocol("WM_DELETE_WINDOW", self._close_detail_window)

    def _close_detail_window(self):
        if self.detail_window:
            self.detail_window.destroy()
            self.detail_window = None
