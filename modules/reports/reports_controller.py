from . import reports_model as model
from .daily_detail_view import DailyDetailView
from datetime import datetime

class ReportsController:
    def __init__(self, app_view):
        self.app_view = app_view
        self.reports_view = None
        self.detail_window = None
        self.data_loaded = {"daily": False, "product": False, "profit": False}

    def set_view(self, view):
        self.reports_view = view
        self.reports_view.set_controller(self)

    def load_data(self):
        """Carga los datos para la pestaña inicial (Resumen Diario)."""
        self.load_daily_summary_data()

    def on_tab_changed(self, event):
        """Se activa cuando el usuario cambia de pestaña."""
        selected_tab_index = self.reports_view.notebook.index(self.reports_view.notebook.select())
        
        if selected_tab_index == 0: # Pestaña de Resumen Diario
            if not self.data_loaded["daily"]:
                self.load_daily_summary_data()
        elif selected_tab_index == 1: # Pestaña de Ventas por Producto
            if not self.data_loaded["product"]:
                self.load_product_sales_data()
        elif selected_tab_index == 2: # Pestaña de Resumen de Ganancias
            # Siempre recargamos las ganancias por si se registró un nuevo gasto o venta
            self.load_profit_summary_data()

    def load_daily_summary_data(self):
        if not self.reports_view: return
        self.reports_view.clear_daily_summary_tree()
        daily_summary = model.get_daily_sales_summary()
        total_revenue = 0
        for item in daily_summary:
            self.reports_view.add_daily_summary_to_tree(item)
            total_revenue += item.get('total_vendido', 0)
        self.reports_view.update_summary_footer(total_revenue)
        self.data_loaded["daily"] = True

    def load_product_sales_data(self):
        if not self.reports_view: return
        self.reports_view.clear_product_sales_tree()
        product_sales = model.get_sales_by_product()
        for item in product_sales:
            self.reports_view.add_product_sale_to_tree(item)
        self.data_loaded["product"] = True

    def load_profit_summary_data(self):
        """Carga los datos para la pestaña de Resumen de Ganancias."""
        if not self.reports_view: return
        summary_data = model.get_profit_summary()
        self.reports_view.update_profit_summary(summary_data)
        self.data_loaded["profit"] = True

    def show_daily_details(self, event=None):
        if not self.reports_view: return
        selected_date_str = self.reports_view.get_selected_date()
        if not selected_date_str: return
        
        try:
            sale_date = datetime.strptime(selected_date_str, '%d/%m/%Y').date()
        except ValueError:
            return
            
        if self.detail_window and self.detail_window.winfo_exists():
            self.detail_window.focus()
            return
            
        sales_data = model.get_sales_details_for_date(sale_date)
        self.detail_window = DailyDetailView(self.app_view, sales_data, sale_date)
        self.detail_window.protocol("WM_DELETE_WINDOW", self._close_detail_window)

    def _close_detail_window(self):
        if self.detail_window:
            self.detail_window.destroy()
            self.detail_window = None
