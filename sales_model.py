from database import get_db_connection
from mysql.connector import Error

def record_sale(cart_data, total, client_id=None, user_id=None):
    """
    Registra una venta, incluyendo el ID del cliente (opcional) y el ID del usuario.
    Utiliza el precio especial (price_override) si existe en el carrito.
    """
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor()
    id_venta = None
    try:
        conn.start_transaction()
        query_venta = "INSERT INTO ventas (id_cliente, id_usuario, total) VALUES (%s, %s, %s)"
        cursor.execute(query_venta, (client_id, user_id, total))
        id_venta = cursor.lastrowid

        query_detalle = "INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)"
        query_update_stock = "UPDATE productos SET stock = stock - %s WHERE id = %s"
        
        for product_id, item in cart_data.items():
            product = item['data']
            quantity = item['qty']
            
            # CORRECCIÓN CLAVE: Usar el precio especial si existe, de lo contrario, el de la BD.
            final_price = item.get('price_override', product['precio_venta'])
            
            if quantity > product['stock']:
                raise Error(f"Stock insuficiente para {product['nombre']}")
                
            cursor.execute(query_detalle, (id_venta, product['id'], quantity, final_price))
            cursor.execute(query_update_stock, (quantity, product['id']))

        conn.commit()
        return id_venta
    except Error as e:
        print(f"Error en transacción de venta: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close(); conn.close()

def get_sale_details_for_receipt(sale_id):
    """
    Recupera todos los detalles para un recibo, incluyendo el nombre del vendedor.
    """
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor(dictionary=True)
    receipt_data = {}
    try:
        query_sale = """
            SELECT v.id, v.fecha, v.total, 
                   c.nombre as cliente_nombre, 
                   u.nombre_completo as vendedor_nombre
            FROM ventas v
            LEFT JOIN clientes c ON v.id_cliente = c.id
            LEFT JOIN usuarios u ON v.id_usuario = u.id
            WHERE v.id = %s;
        """
        cursor.execute(query_sale, (sale_id,))
        receipt_data = cursor.fetchone()
        if not receipt_data: return None

        query_items = """
            SELECT d.cantidad, d.precio_unitario, p.nombre as producto_nombre
            FROM detalle_ventas d JOIN productos p ON d.id_producto = p.id
            WHERE d.id_venta = %s;
        """
        cursor.execute(query_items, (sale_id,))
        receipt_data['items'] = cursor.fetchall()
        return receipt_data
    except Error as e:
        print(f"Error al obtener detalles del recibo: {e}")
        return None
    finally:
        cursor.close(); conn.close()
