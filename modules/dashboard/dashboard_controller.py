from . import dashboard_model as model

class DashboardController:
    def __init__(self, main_app_instance):
        self.main_app = main_app_instance
        self.dashboard_view = main_app_instance.views.get('dashboard')
        if self.dashboard_view:
            self.dashboard_view.set_controller(self)

    def load_data(self):
        """
        Carga los datos desde el modelo y los envía a la vista
        para ser mostrados.
        """
        if not self.dashboard_view:
            return

        # 1. Obtener los datos del modelo
        data = model.get_dashboard_data()
        
        # 2. Enviar los datos a la vista para que se actualice
        if data:
            self.dashboard_view.update_data(data)
