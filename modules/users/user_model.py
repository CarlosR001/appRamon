from database import get_db_connection
from mysql.connector import Error
from auth import hash_password

def get_all_users_with_roles():
    """Recupera todos los usuarios con el nombre de su rol."""
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    query = "SELECT u.id, u.nombre_usuario, u.nombre_completo, r.nombre_rol, u.id_rol FROM usuarios u JOIN roles r ON u.id_rol = r.id ORDER BY u.nombre_usuario;"
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener usuarios: {e}"); return []
    finally:
        cursor.close(); conn.close()

def get_all_roles():
    """Recupera todos los roles disponibles."""
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, nombre_rol FROM roles")
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener roles: {e}"); return []
    finally:
        cursor.close(); conn.close()

def add(data):
    """Añade un nuevo usuario."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    hashed_pass = hash_password(data['password'])
    query = "INSERT INTO usuarios (nombre_usuario, password_hash, id_rol, nombre_completo) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(query, (data['nombre_usuario'], hashed_pass, data['id_rol'], data['nombre_completo']))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al añadir usuario: {e}"); conn.rollback(); return False
    finally:
        cursor.close(); conn.close()
        
def update(user_id, data):
    """Actualiza el nombre completo y el rol de un usuario."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    query = "UPDATE usuarios SET nombre_completo = %s, id_rol = %s WHERE id = %s"
    try:
        cursor.execute(query, (data['nombre_completo'], data['id_rol'], user_id))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al actualizar usuario: {e}"); conn.rollback(); return False
    finally:
        cursor.close(); conn.close()

def update_password(user_id, new_password):
    """Actualiza la contraseña de un usuario."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    hashed_pass = hash_password(new_password)
    try:
        cursor.execute("UPDATE usuarios SET password_hash = %s WHERE id = %s", (hashed_pass, user_id))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al cambiar contraseña: {e}"); conn.rollback(); return False
    finally:
        cursor.close(); conn.close()

def delete(user_id):
    """Elimina un usuario."""
    if user_id == 1: return False # Proteger al admin principal
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al eliminar usuario: {e}"); conn.rollback(); return False
    finally:
        cursor.close(); conn.close()

def get_all_permissions():
    """Obtiene la lista completa de todos los permisos posibles."""
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, nombre_permiso, descripcion FROM permisos ORDER BY id")
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener todos los permisos: {e}"); return []
    finally:
        cursor.close(); conn.close()

def get_permissions_for_role(role_id):
    """Obtiene los IDs de los permisos que un rol ya tiene."""
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_permiso FROM rol_permisos WHERE id_rol = %s", (role_id,))
        return [item[0] for item in cursor.fetchall()]
    except Error as e:
        print(f"Error al obtener permisos del rol: {e}"); return []
    finally:
        cursor.close(); conn.close()

def update_role_permissions(role_id, permission_ids):
    """Actualiza la lista completa de permisos para un rol (transacción)."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        conn.start_transaction()
        # 1. Borrar todos los permisos antiguos para este rol
        cursor.execute("DELETE FROM rol_permisos WHERE id_rol = %s", (role_id,))
        # 2. Insertar los nuevos permisos
        if permission_ids:
            query = "INSERT INTO rol_permisos (id_rol, id_permiso) VALUES (%s, %s)"
            data = [(role_id, p_id) for p_id in permission_ids]
            cursor.executemany(query, data)
        conn.commit()
        return True
    except Error as e:
        print(f"Error al actualizar permisos del rol: {e}"); conn.rollback(); return False
    finally:
        cursor.close(); conn.close()
