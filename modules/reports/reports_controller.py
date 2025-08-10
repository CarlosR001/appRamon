from . import reports_model as model
from .daily_detail_view import DailyDetailView
from datetime import datetime

class ReportsController:
    def __init__(self, app_view):
        self.app_view = app_view
        self.reports_view = None
        self.detail_window = None

    def set_view(self, view):
        self.reports_view = view
        self.reports_view.set_controller(self)

    def load_data(self):
        """Carga los datos para la pestaña inicial (Resumen Diario) sin filtro."""
        self.load_daily_summary_data(use_filter=False)

    def on_tab_changed(self, event):
        """Se activa cuando el usuario cambia de pestaña para una carga inicial."""
        selected_tab_index = self.reports_view.notebook.index(self.reports_view.notebook.select())
        if selected_tab_index == 0:
            self.load_daily_summary_data(use_filter=False)
        elif selected_tab_index == 1:
            self.load_product_sales_data()
        elif selected_tab_index == 2:
            self.load_profit_summary_data(use_filter=False)

    def load_daily_summary_data(self, use_filter=True):
        if not self.reports_view: return
        start_date, end_date = None, None
        if use_filter:
            try:
                start_date = self.reports_view.start_date_entry.get_date()
                end_date = self.reports_view.end_date_entry.get_date()
            except AttributeError: # tkcalendar no instalado
                pass
        
        self.reports_view.clear_daily_summary_tree()
        daily_summary = model.get_daily_sales_summary(start_date, end_date)
        total_revenue = sum(item.get('total_vendido', 0) for item in daily_summary)
        for item in daily_summary:
            self.reports_view.add_daily_summary_to_tree(item)
        self.reports_view.update_summary_footer(total_revenue)

    def load_product_sales_data(self):
        if not self.reports_view: return
        self.reports_view.clear_product_sales_tree()
        product_sales = model.get_sales_by_product()
        for item in product_sales:
            self.reports_view.add_product_sale_to_tree(item)

    def load_profit_summary_data(self, use_filter=True):
        if not self.reports_view: return
        start_date, end_date = None, None
        if use_filter:
            try:
                start_date = self.reports_view.profit_start_date.get_date()
                end_date = self.reports_view.profit_end_date.get_date()
            except AttributeError: # tkcalendar no instalado
                pass
        
        summary_data = model.get_profit_summary(start_date, end_date)
        self.reports_view.update_profit_summary(summary_data)

    def show_daily_details(self, event=None):
        if not self.reports_view: return
        selected_date_str = self.reports_view.get_selected_date()
        if not selected_date_str: return
        
        try:
            sale_date = datetime.strptime(selected_date_str, '%d/%m/%Y').date()
        except ValueError: return
            
        if self.detail_window and self.detail_window.winfo_exists():
            self.detail_window.focus(); return
            
        sales_data = model.get_sales_details_for_date(sale_date)
        self.detail_window = DailyDetailView(self.app_view, sales_data, sale_date)
        self.detail_window.protocol("WM_DELETE_WINDOW", self._close_detail_window)

    def _close_detail_window(self):
        if self.detail_window:
            self.detail_window.destroy()
            self.detail_window = None
