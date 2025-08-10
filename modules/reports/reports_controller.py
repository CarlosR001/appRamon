from . import reports_model as model
from .daily_detail_view import DailyDetailView
from modules.printing import pdf_generator
from datetime import datetime, date
from tkinter import messagebox

# Importamos la bandera para saber si el calendario está disponible
try:
    from .reports_view import calendar_available
except ImportError:
    calendar_available = False

class ReportsController:
    def __init__(self, app_view):
        self.app_view = app_view
        self.reports_view = None
        self.detail_window = None
        self.last_cash_balance_data = None

    def set_view(self, view):
        self.reports_view = view
        self.reports_view.set_controller(self)

    def _get_dates_from_filter(self, start_widget, end_widget):
        """Función auxiliar robusta para obtener fechas de los widgets."""
        try:
            if calendar_available:
                return start_widget.get_date(), end_widget.get_date()
            else: # Fallback si se usan ttk.Entry
                start_date = datetime.strptime(start_widget.get(), '%d/%m/%Y').date()
                end_date = datetime.strptime(end_widget.get(), '%d/%m/%Y').date()
                return start_date, end_date
        except (ValueError, AttributeError):
            messagebox.showerror("Formato de Fecha Inválido", "Por favor, use el formato DD/MM/YYYY.", parent=self.app_view)
            return None, None

    def load_data(self):
        self.load_daily_summary_data(use_filter=False)

    def on_tab_changed(self, event):
        selected_tab_index = self.reports_view.notebook.index(self.reports_view.notebook.select())
        # Cargar datos solo la primera vez que se visita la pestaña, o si se pulsa el botón
        if selected_tab_index == 0: self.load_daily_summary_data(use_filter=False)
        elif selected_tab_index == 1: self.load_product_sales_data()
        elif selected_tab_index == 2: self.load_profit_summary_data(use_filter=False)
        elif selected_tab_index == 3: self.load_cash_balance_data()

    def load_daily_summary_data(self, use_filter=True):
        if not self.reports_view: return
        start_date, end_date = None, None
        if use_filter and calendar_available:
            start_date, end_date = self._get_dates_from_filter(self.reports_view.start_date_entry, self.reports_view.end_date_entry)
            if start_date is None: return
        
        self.reports_view.clear_daily_summary_tree()
        daily_summary = model.get_daily_sales_summary(start_date, end_date)
        total_revenue = sum(item.get('total_vendido', 0) for item in daily_summary)
        for item in daily_summary: self.reports_view.add_daily_summary_to_tree(item)
        self.reports_view.update_summary_footer(total_revenue)

    def load_product_sales_data(self):
        if not self.reports_view: return
        self.reports_view.clear_product_sales_tree()
        product_sales = model.get_sales_by_product()
        for item in product_sales: self.reports_view.add_product_sale_to_tree(item)

    def load_profit_summary_data(self, use_filter=True):
        if not self.reports_view: return
        start_date, end_date = None, None
        if use_filter and calendar_available:
            start_date, end_date = self._get_dates_from_filter(self.reports_view.profit_start_date, self.reports_view.profit_end_date)
            if start_date is None: return
        
        summary_data = model.get_profit_summary(start_date, end_date)
        self.reports_view.update_profit_summary(summary_data)

    def load_cash_balance_data(self):
        if not self.reports_view: return
        balance_date = None
        try:
            if calendar_available:
                balance_date = self.reports_view.cash_balance_date.get_date()
            else: # Fallback para ttk.Entry
                balance_date_str = self.reports_view.cash_balance_date.get()
                balance_date = datetime.strptime(balance_date_str, '%d/%m/%Y').date()

            balance_data = model.get_cash_balance_for_date(balance_date)
            if balance_data:
                self.reports_view.update_cash_balance(balance_data)
                self.last_cash_balance_data = balance_data
                self.last_cash_balance_data['date'] = balance_date
        except (ValueError, AttributeError):
             messagebox.showerror("Formato de Fecha Inválido", "Por favor, use el formato DD/MM/YYYY.", parent=self.app_view)
        except Exception as e:
            print(f"Error al cargar cuadre de caja: {e}")

    def print_cash_balance(self):
        if self.last_cash_balance_data:
            pdf_generator.generate_cash_balance_report(self.last_cash_balance_data)
        else:
            messagebox.showinfo("Sin Datos", "Por favor, genere un cuadre de caja primero antes de imprimir.", parent=self.app_view)

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
