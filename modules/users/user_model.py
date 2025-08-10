from database import get_db_connection
from mysql.connector import Error
from auth import hash_password

def get_all_users_with_roles():
    """Recupera todos los usuarios con el nombre de su rol."""
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT u.id, u.nombre_usuario, u.nombre_completo, r.nombre_rol
        FROM usuarios u
        JOIN roles r ON u.id_rol = r.id
        ORDER BY u.nombre_usuario;
    """
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener usuarios: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_all_roles():
    """Recupera todos los roles disponibles."""
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, nombre_rol FROM roles")
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener roles: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def add(data):
    """Añade un nuevo usuario."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    hashed_pass = hash_password(data['password'])
    query = """
        INSERT INTO usuarios (nombre_usuario, password_hash, id_rol, nombre_completo)
        VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (data['nombre_usuario'], hashed_pass, data['id_rol'], data['nombre_completo']))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al añadir usuario: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def delete(user_id):
    """Elimina un usuario."""
    # Prevenir que el admin principal (ID 1) se elimine a sí mismo.
    if user_id == 1:
        return False
        
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al eliminar usuario: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# Nota: Las funciones para editar usuarios (cambiar rol, nombre, contraseña)
# se pueden añadir aquí en una futura mejora si es necesario.
# Por simplicidad, el flujo inicial se centrará en crear y eliminar.
