from database import get_db_connection
from mysql.connector import Error

def get_by_id(service_id):
    """Recupera todos los detalles de una orden de servicio específica por su ID."""
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT s.*, c.nombre as nombre_cliente, c.telefono as telefono_cliente FROM servicios s JOIN clientes c ON s.id_cliente = c.id WHERE s.id = %s;"
        cursor.execute(query, (service_id,))
        service_data = cursor.fetchone()
        if service_data:
            query_items_cost = "SELECT SUM(cantidad * precio_venta_unitario) as total_items_cost FROM detalle_servicios WHERE id_servicio = %s;"
            cursor.execute(query_items_cost, (service_id,))
            items_cost_result = cursor.fetchone()
            service_data['total_items_cost'] = float(items_cost_result['total_items_cost']) if items_cost_result and items_cost_result['total_items_cost'] else 0.0
        return service_data
    except Error as e:
        print(f"Error al obtener la orden de servicio por ID: {e}")
        return None
    finally:
        cursor.close(); conn.close()

def get_all():
    """Recupera todas las órdenes de servicio."""
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    query = "SELECT s.id, s.descripcion_equipo, s.problema_reportado, s.fecha_recepcion, s.estado, c.nombre as nombre_cliente, c.telefono as telefono_cliente FROM servicios s JOIN clientes c ON s.id_cliente = c.id ORDER BY s.fecha_recepcion DESC;"
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener las órdenes de servicio: {e}")
        return []
    finally:
        cursor.close(); conn.close()

def add(data):
    """Añade una nueva orden de servicio."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    query = "INSERT INTO servicios (id_cliente, descripcion_equipo, problema_reportado, estado) VALUES (%s, %s, %s, 'Recibido')"
    try:
        cursor.execute(query, (data['id_cliente'], data['descripcion_equipo'], data['problema_reportado']))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al añadir la orden de servicio: {e}"); conn.rollback(); return False
    finally:
        cursor.close(); conn.close()

def update_status_and_cost(service_id, new_status, service_cost):
    """Actualiza solo el estado y el costo del servicio (mano de obra)."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    query = "UPDATE servicios SET estado = %s, costo_servicio = %s WHERE id = %s"
    try:
        cursor.execute(query, (new_status, service_cost, service_id))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al actualizar la orden de servicio: {e}"); conn.rollback(); return False
    finally:
        cursor.close(); conn.close()

def get_service_items(service_id):
    """Obtiene todos los productos/repuestos asociados a un servicio (CORREGIDO)."""
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT ds.id, ds.id_producto, ds.cantidad, ds.precio_venta_unitario, p.nombre
        FROM detalle_servicios ds JOIN productos p ON ds.id_producto = p.id
        WHERE ds.id_servicio = %s;
    """
    try:
        cursor.execute(query, (service_id,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener los items del servicio: {e}")
        return []
    finally:
        cursor.close(); conn.close()

def add_item_to_service(service_id, product, quantity):
    """Añade un item (producto) a un servicio y descuenta el stock (transacción)."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        conn.start_transaction()
        query_add = "INSERT INTO detalle_servicios (id_servicio, id_producto, cantidad, precio_venta_unitario) VALUES (%s, %s, %s, %s)"
        cursor.execute(query_add, (service_id, product['id'], quantity, product['precio_venta']))
        query_stock = "UPDATE productos SET stock = stock - %s WHERE id = %s"
        cursor.execute(query_stock, (quantity, product['id']))
        conn.commit()
        return True
    except Error as e:
        print(f"Error en la transacción al añadir item: {e}"); conn.rollback(); return False
    finally:
        cursor.close(); conn.close()

def remove_item_from_service(detail_id, product_id, quantity):
    """Elimina un item de un servicio y restaura el stock (transacción)."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        conn.start_transaction()
        cursor.execute("DELETE FROM detalle_servicios WHERE id = %s", (detail_id,))
        query_stock = "UPDATE productos SET stock = stock + %s WHERE id = %s"
        cursor.execute(query_stock, (quantity, product_id))
        conn.commit()
        return True
    except Error as e:
        print(f"Error en la transacción al eliminar item: {e}"); conn.rollback(); return False
    finally:
        cursor.close(); conn.close()
