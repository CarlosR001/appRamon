-- SQL SCRIPT PARA UNA INSTALACIÓN LIMPIA DE ELECTRO-PRO
-- Ejecutar este script en una base de datos MySQL vacía (ej. 'tienda_electronica')

-- Eliminar tablas en orden si ya existen para una reinstalación limpia
DROP TABLE IF EXISTS `detalle_servicios`, `detalle_compras`, `detalle_ventas`, `compras`, `ventas`, `servicios`, `gastos`, `productos`, `proveedores`, `clientes`, `rol_permisos`, `permisos`, `usuarios`, `roles`, `categorias`;

-- Estructura de Tablas
CREATE TABLE `categorias` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
);

CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_rol` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre_rol` (`nombre_rol`)
);

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_usuario` varchar(50) NOT NULL,
  `password_hash` varchar(256) NOT NULL,
  `id_rol` int(11) DEFAULT NULL,
  `nombre_completo` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre_usuario` (`nombre_usuario`),
  KEY `id_rol` (`id_rol`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id`)
);

CREATE TABLE `clientes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `proveedores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `productos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(50) DEFAULT NULL,
  `nombre` varchar(150) NOT NULL,
  `descripcion` text,
  `precio_compra` decimal(10,2) NOT NULL,
  `precio_venta` decimal(10,2) NOT NULL,
  `stock` int(11) NOT NULL DEFAULT '0',
  `id_categoria` int(11) DEFAULT NULL,
  `id_proveedor` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo` (`codigo`),
  KEY `id_categoria` (`id_categoria`),
  KEY `id_proveedor` (`id_proveedor`),
  CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id`),
  CONSTRAINT `productos_ibfk_2` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id`)
);

CREATE TABLE `gastos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(255) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `fecha` date NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `servicios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` int(11) NOT NULL,
  `descripcion_equipo` varchar(255) DEFAULT NULL,
  `problema_reportado` text NOT NULL,
  `fecha_recepcion` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_entrega` datetime DEFAULT NULL,
  `estado` enum('Recibido','En Diagnostico','Esperando Piezas','En Reparacion','Listo','Entregado') NOT NULL,
  `costo_servicio` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`id`),
  KEY `id_cliente` (`id_cliente`),
  CONSTRAINT `servicios_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`)
);

CREATE TABLE `ventas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` int(11) DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `total` decimal(10,2) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `estado` varchar(20) NOT NULL DEFAULT 'Completada',
  PRIMARY KEY (`id`),
  KEY `id_cliente` (`id_cliente`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`),
  CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`)
);

CREATE TABLE `compras` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_proveedor` int(11) DEFAULT NULL,
  `fecha_compra` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `total_compra` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_proveedor` (`id_proveedor`),
  CONSTRAINT `compras_ibfk_1` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id`)
);

CREATE TABLE `detalle_compras` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_compra` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `costo_unitario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_compra` (`id_compra`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `detalle_compras_ibfk_1` FOREIGN KEY (`id_compra`) REFERENCES `compras` (`id`),
  CONSTRAINT `detalle_compras_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id`)
);

CREATE TABLE `detalle_ventas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_venta` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_venta` (`id_venta`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `detalle_ventas_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id`),
  CONSTRAINT `detalle_ventas_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id`)
);

CREATE TABLE `detalle_servicios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_servicio` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_venta_unitario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_servicio` (`id_servicio`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `detalle_servicios_ibfk_1` FOREIGN KEY (`id_servicio`) REFERENCES `servicios` (`id`),
  CONSTRAINT `detalle_servicios_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id`)
);

CREATE TABLE `permisos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_permiso` varchar(100) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre_permiso` (`nombre_permiso`)
);

CREATE TABLE `rol_permisos` (
  `id_rol` int(11) NOT NULL,
  `id_permiso` int(11) NOT NULL,
  PRIMARY KEY (`id_rol`,`id_permiso`),
  KEY `id_permiso` (`id_permiso`),
  CONSTRAINT `rol_permisos_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id`),
  CONSTRAINT `rol_permisos_ibfk_2` FOREIGN KEY (`id_permiso`) REFERENCES `permisos` (`id`)
);

-- Datos Esenciales (Semilla)
INSERT INTO `categorias` (`nombre`) VALUES
('Componentes'),
('Periféricos'),
('Audio y Video'),
('Cables y Adaptadores'),
('Servicios');

INSERT INTO `roles` (`nombre_rol`) VALUES
('Administrador'),
('Vendedor'),
('Técnico');

INSERT INTO `usuarios` (`nombre_usuario`, `password_hash`, `id_rol`, `nombre_completo`) VALUES
('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 1, 'Administrador del Sistema');

INSERT INTO `permisos` (`nombre_permiso`, `descripcion`) VALUES
('access_dashboard', 'Acceder al Dashboard'),
('access_sales', 'Acceder al TPV de Ventas'),
('access_purchases', 'Acceder al módulo de Compras'),
('access_inventory', 'Acceder al Inventario'),
('access_clients', 'Acceder a Clientes'),
('access_services', 'Acceder a Servicios'),
('access_sales_history', 'Acceder al Historial de Ventas y anular ventas'),
('access_suppliers', 'Acceder a Proveedores'),
('access_expenses', 'Acceder a Gastos'),
('access_reports', 'Acceder a todos los Reportes'),
('access_users', 'Acceder a la Gestión de Usuarios');

INSERT INTO `rol_permisos` (`id_rol`, `id_permiso`)
SELECT 1, id FROM permisos;

INSERT INTO `rol_permisos` (`id_rol`, `id_permiso`)
SELECT 2, id FROM permisos WHERE nombre_permiso IN (
    'access_dashboard',
    'access_sales',
    'access_inventory',
    'access_clients',
    'access_purchases'
);

INSERT INTO `rol_permisos` (`id_rol`, `id_permiso`)
SELECT 3, id FROM permisos WHERE nombre_permiso IN (
    'access_dashboard',
    'access_inventory',
    'access_clients',
    'access_services'
);
