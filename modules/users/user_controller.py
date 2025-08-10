from tkinter import messagebox
from . import user_model as model

class UserController:
    def __init__(self, main_app_instance):
        self.main_app = main_app_instance
        self.users_view = main_app_instance.views.get('users')
        if self.users_view:
            self.users_view.set_controller(self)

    def load_initial_data(self):
        """Carga todos los datos necesarios cuando se muestra la vista."""
        if not self.users_view: return
        
        # Cargar roles y pasarlos a la vista para el combobox
        roles = model.get_all_roles()
        self.users_view.set_roles(roles)

        # Cargar la lista de usuarios
        self.load_all_users()

    def load_all_users(self):
        """Carga todos los usuarios del modelo y los muestra en la vista."""
        if not self.users_view: return
        self.users_view.clear_tree()
        users = model.get_all_users_with_roles()
        for user in users:
            self.users_view.insert_user(user)

    def add_user(self):
        """Añade un nuevo usuario a la base de datos."""
        if not self.users_view: return
        
        data = self.users_view.get_user_data()
        if data:
            if model.add(data):
                messagebox.showinfo("Éxito", "Usuario creado correctamente.", parent=self.main_app)
                self.users_view.clear_form()
                self.load_all_users() # Refrescar la lista
            else:
                messagebox.showerror("Error", "No se pudo crear el usuario. ¿Quizás el nombre de usuario ya existe?", parent=self.main_app)

    def delete_user(self):
        """Elimina el usuario seleccionado."""
        if not self.users_view: return
        
        user_id = self.users_view.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Sin Selección", "Por favor, seleccione un usuario de la lista para eliminar.", parent=self.main_app)
            return
            
        if int(user_id) == 1:
            messagebox.showerror("Acción no permitida", "No puede eliminar al usuario administrador principal.", parent=self.main_app)
            return

        if messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar a este usuario?", parent=self.main_app):
            if model.delete(user_id):
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente.", parent=self.main_app)
                self.load_all_users()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario.", parent=self.main_app)
