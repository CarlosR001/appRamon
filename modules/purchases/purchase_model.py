from database import get_db_connection
from mysql.connector import Error

def record_purchase(cart_data, total, supplier_id):
    """
    Registra una compra y recalcula el costo promedio ponderado de cada producto.
    Esto se ejecuta como una transacción para garantizar la integridad de los datos.
    """
    conn = get_db_connection()
    if not conn:
        return False

    cursor = conn.cursor(dictionary=True)
    id_compra = None

    try:
        conn.start_transaction()

        # 1. Insertar la cabecera de la compra
        query_compra = "INSERT INTO compras (id_proveedor, total_compra) VALUES (%s, %s)"
        cursor.execute(query_compra, (supplier_id, total))
        id_compra = cursor.lastrowid

        # 2. Iterar sobre cada producto del carrito para procesarlo
        query_get_product = "SELECT stock, precio_compra FROM productos WHERE id = %s FOR UPDATE"
        query_detalle = "INSERT INTO detalle_compras (id_compra, id_producto, cantidad, costo_unitario) VALUES (%s, %s, %s, %s)"
        query_update_product = "UPDATE productos SET stock = %s, precio_compra = %s WHERE id = %s"

        for product_id, item in cart_data.items():
            # Obtener el estado actual del producto (bloqueando la fila para la transacción)
            cursor.execute(query_get_product, (product_id,))
            current_product = cursor.fetchone()
            
            if not current_product:
                # Si el producto no existe por alguna razón, cancelar todo.
                raise Error(f"El producto con ID {product_id} no fue encontrado.")

            old_stock = current_product.get('stock', 0)
            old_cost = float(current_product.get('precio_compra', 0.0))
            
            new_stock_qty = item['qty']
            new_purchase_cost = float(item['cost'])

            # --- Aplicar la fórmula del Costo Promedio Ponderado ---
            total_stock = old_stock + new_stock_qty
            if total_stock > 0:
                new_avg_cost = ((old_stock * old_cost) + (new_stock_qty * new_purchase_cost)) / total_stock
            else:
                new_avg_cost = new_purchase_cost # Caso inicial si el stock era 0

            # Insertar el detalle de la compra con el costo de ESE momento
            cursor.execute(query_detalle, (id_compra, product_id, new_stock_qty, new_purchase_cost))
            
            # Actualizar el producto con el nuevo stock y el NUEVO costo promedio
            cursor.execute(query_update_product, (total_stock, new_avg_cost, product_id))

        conn.commit()
        return True

    except Error as e:
        print(f"Error en la transacción de compra: {e}")
        conn.rollback()
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
