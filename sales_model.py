from database import get_db_connection
from mysql.connector import Error

def record_sale(cart_data, total, client_id=None):
    """
    Registra una venta en la base de datos como una transacción.
    Devuelve el ID de la nueva venta si tiene éxito, o None si falla.
    """
    conn = get_db_connection()
    if not conn:
        return None

    cursor = conn.cursor()
    id_venta = None

    try:
        conn.start_transaction()
        query_venta = "INSERT INTO ventas (id_cliente, total) VALUES (%s, %s)"
        cursor.execute(query_venta, (client_id, total))
        id_venta = cursor.lastrowid

        query_detalle = "INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)"
        query_update_stock = "UPDATE productos SET stock = stock - %s WHERE id = %s"
        
        for product_id, item in cart_data.items():
            product = item['data']
            quantity = item['qty']
            
            if quantity > product['stock']:
                raise Error(f"Stock insuficiente para el producto: {product['nombre']}")

            cursor.execute(query_detalle, (id_venta, product['id'], quantity, product['precio_venta']))
            cursor.execute(query_update_stock, (quantity, product['id']))

        conn.commit()
        return id_venta

    except Error as e:
        print(f"Error en la transacción de venta: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def get_sale_details_for_receipt(sale_id):
    """
    Recupera todos los detalles necesarios para un recibo a partir de un ID de venta.
    """
    conn = get_db_connection()
    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)
    receipt_data = {}

    try:
        # Obtener información general de la venta y del cliente (si existe)
        query_sale = """
            SELECT v.id, v.fecha, v.total, c.nombre as cliente_nombre, c.telefono as cliente_telefono
            FROM ventas v
            LEFT JOIN clientes c ON v.id_cliente = c.id
            WHERE v.id = %s;
        """
        cursor.execute(query_sale, (sale_id,))
        receipt_data = cursor.fetchone()

        if not receipt_data:
            return None

        # Obtener los productos de esa venta
        query_items = """
            SELECT d.cantidad, d.precio_unitario, p.nombre as producto_nombre
            FROM detalle_ventas d
            JOIN productos p ON d.id_producto = p.id
            WHERE d.id_venta = %s;
        """
        cursor.execute(query_items, (sale_id,))
        receipt_data['items'] = cursor.fetchall()

        return receipt_data

    except Error as e:
        print(f"Error al obtener los detalles del recibo: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
