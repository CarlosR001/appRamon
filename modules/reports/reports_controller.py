from . import reports_model as model

class ReportsController:
    def __init__(self, app_view):
        self.app_view = app_view
        # La vista de reportes se asignará cuando el usuario navegue a ella
        self.reports_view = None

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

        # 1. Limpiar la vista antes de cargar nuevos datos
        self.reports_view.clear_tree()

        # 2. Obtener los datos del modelo
        daily_summary = model.get_daily_sales_summary()

        # 3. Procesar los datos y enviarlos a la vista
        total_revenue = 0
        for item in daily_summary:
            self.reports_view.add_daily_summary_to_tree(item)
            total_revenue += item.get('total_vendido', 0)
            
        # 4. Actualizar el pie de página con el total general
        self.reports_view.update_summary_footer(total_revenue)
