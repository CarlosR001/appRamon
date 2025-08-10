import hashlib
from database import get_db_connection
from mysql.connector import Error

def hash_password(password):
    """Genera un hash SHA-256 para una contraseña dada."""
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_permissions(user_role_id):
    """Obtiene la lista de permisos para un ID de rol específico."""
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor()
    query = """
        SELECT p.nombre_permiso 
        FROM rol_permisos rp
        JOIN permisos p ON rp.id_permiso = p.id
        WHERE rp.id_rol = %s;
    """
    try:
        cursor.execute(query, (user_role_id,))
        permissions = [row[0] for row in cursor.fetchall()]
        return permissions
    except Error as e:
        print(f"Error al obtener permisos: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def verify_and_get_user(username, provided_password):
    """
    Verifica las credenciales y, si son correctas, devuelve los datos del usuario,
    incluyendo su lista de permisos.
    """
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id, password_hash, id_rol FROM usuarios WHERE nombre_usuario = %s", (username,))
        user_data = cursor.fetchone()
        
        if user_data and user_data['password_hash'] == hash_password(provided_password):
            # Contraseña correcta, obtener permisos
            permissions = get_user_permissions(user_data['id_rol'])
            user_data['permissions'] = permissions
            return user_data
        else:
            # Usuario no encontrado o contraseña incorrecta
            return None
    except Error as e:
        print(f"Error al verificar usuario: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
