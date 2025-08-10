from tkinter import messagebox, simpledialog
from . import user_model as model

class UserController:
    def __init__(self, main_app_instance):
        self.main_app = main_app_instance
        self.users_view = main_app_instance.views.get('users')
        if self.users_view:
            self.users_view.set_controller(self)

    def load_initial_data(self):
        if not self.users_view: return
        self.load_all_users()
        roles = model.get_all_roles()
        self.users_view.set_roles(roles)

    def load_all_users(self):
        self.users_view.clear_user_tree()
        users = model.get_all_users_with_roles()
        for user in users:
            self.users_view.insert_user(user)
        self.users_view.clear_user_form()

    def add_user(self):
        data = self.users_view.get_user_data()
        if data:
            if model.add(data):
                messagebox.showinfo("Éxito", "Usuario creado.", parent=self.main_app)
                self.load_all_users()
            else:
                messagebox.showerror("Error", "No se pudo crear el usuario.", parent=self.main_app)

    def edit_user(self):
        user_id = self.users_view.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Sin Selección", "Seleccione un usuario para editar.", parent=self.main_app); return
        
        user_id = int(user_id)
        if user_id == 1:
            if not messagebox.askyesno("Confirmar", "El usuario 'admin' es especial. Solo se recomienda cambiar su nombre. ¿Continuar?", parent=self.main_app):
                 return # Si el admin dice 'No', salir de la función
        
        data = self.users_view.get_user_data(is_edit=True)
        if not data: return
            
        if model.update(user_id, data):
            if data['password'] and data['password'] != "********":
                model.update_password(user_id, data['password'])
            messagebox.showinfo("Éxito", "Usuario actualizado.", parent=self.main_app)
            self.load_all_users()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el usuario.", parent=self.main_app)

    def delete_user(self):
        user_id = self.users_view.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Sin Selección", "Seleccione un usuario para eliminar.", parent=self.main_app); return
            
        user_id = int(user_id)
        if user_id == 1:
            messagebox.showerror("Acción no permitida", "No puede eliminar al admin principal.", parent=self.main_app); return

        if messagebox.askyesno("Confirmar Eliminación", "¿Está seguro?", parent=self.main_app):
            if model.delete(user_id):
                messagebox.showinfo("Éxito", "Usuario eliminado.", parent=self.main_app)
                self.load_all_users()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario.", parent=self.main_app)

    def on_role_selected(self, event=None):
        role_name = self.users_view.role_select_var.get()
        if not role_name: return
        role = next((r for r in self.users_view.roles if r['nombre_rol'] == role_name), None)
        if not role: return
        all_permissions = model.get_all_permissions()
        role_permissions = model.get_permissions_for_role(role['id'])
        self.users_view.populate_permissions(all_permissions, role_permissions)
        
    def save_role_permissions(self):
        role_name = self.users_view.role_select_var.get()
        if not role_name:
            messagebox.showwarning("Sin Selección", "Seleccione un rol.", parent=self.main_app); return
        role = next((r for r in self.users_view.roles if r['nombre_rol'] == role_name), None)
        if not role: return
        selected_permission_ids = [p_id for p_id, var in self.users_view.permission_vars.items() if var.get()]
        if model.update_role_permissions(role['id'], selected_permission_ids):
            messagebox.showinfo("Éxito", f"Permisos para '{role_name}' actualizados.", parent=self.main_app)
        else:
            messagebox.showerror("Error", "No se pudieron guardar los permisos.", parent=self.main_app)
