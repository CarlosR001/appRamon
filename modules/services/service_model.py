from database import get_db_connection
from mysql.connector import Error

def get_by_id(service_id):
    """Recupera todos los detalles de una orden de servicio específica por su ID."""
    conn = get_db_connection()
    if not conn: return None
    
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            s.*,
            c.nombre as nombre_cliente,
            c.telefono as telefono_cliente
        FROM servicios s
        JOIN clientes c ON s.id_cliente = c.id
        WHERE s.id = %s;
    """
    try:
        cursor.execute(query, (service_id,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error al obtener la orden de servicio por ID: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_all():
    """Recupera todas las órdenes de servicio, uniendo los datos del cliente."""
    conn = get_db_connection()
    if not conn: return []

    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            s.id, s.descripcion_equipo, s.problema_reportado, s.fecha_recepcion, s.estado,
            c.nombre as nombre_cliente, c.telefono as telefono_cliente
        FROM servicios s
        JOIN clientes c ON s.id_cliente = c.id
        ORDER BY s.fecha_recepcion DESC;
    """
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener las órdenes de servicio: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def add(data):
    """Añade una nueva orden de servicio a la base de datos."""
    conn = get_db_connection()
    if not conn: return False
    
    cursor = conn.cursor()
    query = "INSERT INTO servicios (id_cliente, descripcion_equipo, problema_reportado, estado) VALUES (%s, %s, %s, 'Recibido')"
    try:
        cursor.execute(query, (data['id_cliente'], data['descripcion_equipo'], data['problema_reportado']))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al añadir la orden de servicio: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def update(service_id, new_status, final_cost, notes=""):
    """Actualiza el estado y el costo de una orden de servicio."""
    # En una futura mejora, las 'notes' se podrían añadir a una tabla separada.
    # Por ahora, las podríamos concatenar en la descripción del problema si fuera necesario.
    conn = get_db_connection()
    if not conn: return False
    
    cursor = conn.cursor()
    query = "UPDATE servicios SET estado = %s, costo_servicio = %s WHERE id = %s"
    try:
        cursor.execute(query, (new_status, final_cost, service_id))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al actualizar la orden de servicio: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
