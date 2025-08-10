from database import get_db_connection
from mysql.connector import Error

def search(search_term):
    """Busca clientes por nombre o teléfono."""
    conn = get_db_connection()
    if not conn:
        return []
    
    cursor = conn.cursor(dictionary=True)
    like_term = f"%{search_term}%"
    query = """
        SELECT id, nombre, telefono, email, direccion 
        FROM clientes 
        WHERE nombre LIKE %s OR telefono LIKE %s
        ORDER BY nombre
    """
    try:
        cursor.execute(query, (like_term, like_term))
        return cursor.fetchall()
    except Error as e:
        print(f"Error al buscar clientes: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_all():
    """Recupera todos los clientes."""
    return search("")

def add(data):
    """Añade un nuevo cliente."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    query = "INSERT INTO clientes (nombre, telefono, email, direccion) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(query, (data['nombre'], data['telefono'], data['email'], data['direccion']))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al añadir cliente: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def update(client_id, data):
    """Actualiza los datos de un cliente."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    query = """
        UPDATE clientes SET nombre = %s, telefono = %s, email = %s, direccion = %s
        WHERE id = %s
    """
    try:
        cursor.execute(query, (data['nombre'], data['telefono'], data['email'], data['direccion'], client_id))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al actualizar cliente: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def delete(client_id):
    """Elimina un cliente."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM clientes WHERE id = %s", (client_id,))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al eliminar cliente: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
