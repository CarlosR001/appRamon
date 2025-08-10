from database import get_db_connection
from mysql.connector import Error

def record_sale(cart_data, total, client_id=None):
    """
    Registra una venta en la base de datos como una transacción.
    Ahora incluye el ID del cliente (opcional).
    """
    conn = get_db_connection()
    if not conn:
        return False

    cursor = conn.cursor()

    try:
        # Iniciar transacción
        conn.start_transaction()

        # 1. Insertar en la tabla 'ventas', incluyendo el id_cliente
        query_venta = "INSERT INTO ventas (id_cliente, total) VALUES (%s, %s)"
        cursor.execute(query_venta, (client_id, total))
        id_venta = cursor.lastrowid

        # 2. Iterar sobre el carrito para insertar en 'detalle_ventas' y actualizar 'productos'
        query_detalle = """
            INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """
        query_update_stock = """
            UPDATE productos SET stock = stock - %s WHERE id = %s
        """
        
        for product_id, item in cart_data.items():
            product = item['data']
            quantity = item['qty']
            
            # Comprobar si hay suficiente stock antes de continuar
            if quantity > product['stock']:
                # Si no hay suficiente stock para algún producto, cancelamos toda la transacción.
                raise Error(f"Stock insuficiente para el producto: {product['nombre']}")

            # Insertar detalle de venta
            cursor.execute(query_detalle, (id_venta, product['id'], quantity, product['precio_venta']))
            
            # Actualizar stock
            cursor.execute(query_update_stock, (quantity, product['id']))

        # Si todo fue bien, confirmar todos los cambios
        conn.commit()
        return True

    except Error as e:
        print(f"Error en la transacción de venta: {e}")
        # Si algo sale mal, deshacer todos los cambios desde el inicio de la transacción
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
