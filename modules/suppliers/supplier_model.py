from database import get_db_connection
from mysql.connector import Error

def get_by_id(supplier_id):
    """Recupera un proveedor específico por su ID."""
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM proveedores WHERE id = %s", (supplier_id,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error al obtener proveedor por ID: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def search(search_term):
    """Busca proveedores por nombre o teléfono."""
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    like_term = f"%{search_term}%"
    query = "SELECT * FROM proveedores WHERE nombre LIKE %s OR telefono LIKE %s ORDER BY nombre"
    try:
        cursor.execute(query, (like_term, like_term))
        return cursor.fetchall()
    except Error as e:
        print(f"Error al buscar proveedores: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_all():
    """Recupera todos los proveedores."""
    return search("")

def add(data):
    """Añade un nuevo proveedor."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    query = "INSERT INTO proveedores (nombre, telefono, email) VALUES (%s, %s, %s)"
    try:
        cursor.execute(query, (data['nombre'], data['telefono'], data['email']))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al añadir proveedor: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def update(supplier_id, data):
    """Actualiza los datos de un proveedor."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    query = "UPDATE proveedores SET nombre = %s, telefono = %s, email = %s WHERE id = %s"
    try:
        cursor.execute(query, (data['nombre'], data['telefono'], data['email'], supplier_id))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al actualizar proveedor: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def delete(supplier_id):
    """Elimina un proveedor."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM proveedores WHERE id = %s", (supplier_id,))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al eliminar proveedor: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
