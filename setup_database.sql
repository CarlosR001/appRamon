-- SQL SCRIPT PARA UNA INSTALACIÓN LIMPIA Y AUTOMÁTICA CON SQLITE

DROP TABLE IF EXISTS `detalle_servicios`;
DROP TABLE IF EXISTS `detalle_compras`;
DROP TABLE IF EXISTS `detalle_ventas`;
DROP TABLE IF EXISTS `compras`;
DROP TABLE IF EXISTS `ventas`;
DROP TABLE IF EXISTS `servicios`;
DROP TABLE IF EXISTS `gastos`;
DROP TABLE IF EXISTS `productos`;
DROP TABLE IF EXISTS `proveedores`;
DROP TABLE IF EXISTS `clientes`;
DROP TABLE IF EXISTS `rol_permisos`;
DROP TABLE IF EXISTS `permisos`;
DROP TABLE IF EXISTS `usuarios`;
DROP TABLE IF EXISTS `roles`;
DROP TABLE IF EXISTS `categorias`;

CREATE TABLE `categorias` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `nombre` TEXT NOT NULL UNIQUE
);

CREATE TABLE `roles` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `nombre_rol` TEXT NOT NULL UNIQUE
);

CREATE TABLE `usuarios` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `nombre_usuario` TEXT NOT NULL UNIQUE,
  `password_hash` TEXT NOT NULL,
  `id_rol` INTEGER,
  `nombre_completo` TEXT,
  FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id`)
);

CREATE TABLE `clientes` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `nombre` TEXT NOT NULL,
  `telefono` TEXT,
  `email` TEXT,
  `direccion` TEXT
);

CREATE TABLE `proveedores` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `nombre` TEXT NOT NULL,
  `telefono` TEXT,
  `email` TEXT
);

CREATE TABLE `productos` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `codigo` TEXT UNIQUE,
  `nombre` TEXT NOT NULL,
  `descripcion` TEXT,
  `precio_compra` REAL NOT NULL,
  `precio_venta` REAL NOT NULL,
  `stock` INTEGER NOT NULL DEFAULT 0,
  `id_categoria` INTEGER,
  `id_proveedor` INTEGER,
  FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id`),
  FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id`)
);

CREATE TABLE `gastos` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `descripcion` TEXT NOT NULL,
  `monto` REAL NOT NULL,
  `fecha` DATE NOT NULL
);

CREATE TABLE `servicios` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `id_cliente` INTEGER NOT NULL,
  `descripcion_equipo` TEXT,
  `problema_reportado` TEXT NOT NULL,
  `fecha_recepcion` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `fecha_entrega` DATETIME,
  `estado` TEXT NOT NULL,
  `costo_servicio` REAL DEFAULT 0.00,
  FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`)
);

CREATE TABLE `ventas` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `id_cliente` INTEGER,
  `fecha` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `total` REAL NOT NULL,
  `id_usuario` INTEGER,
  `estado` TEXT NOT NULL DEFAULT 'Completada',
  FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`),
  FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`)
);

CREATE TABLE `compras` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `id_proveedor` INTEGER,
  `fecha_compra` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `total_compra` REAL NOT NULL,
  FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id`)
);

CREATE TABLE `detalle_compras` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `id_compra` INTEGER NOT NULL,
  `id_producto` INTEGER NOT NULL,
  `cantidad` INTEGER NOT NULL,
  `costo_unitario` REAL NOT NULL,
  FOREIGN KEY (`id_compra`) REFERENCES `compras` (`id`),
  FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id`)
);

CREATE TABLE `detalle_ventas` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `id_venta` INTEGER NOT NULL,
  `id_producto` INTEGER NOT NULL,
  `cantidad` INTEGER NOT NULL,
  `precio_unitario` REAL NOT NULL,
  FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id`),
  FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id`)
);

CREATE TABLE `detalle_servicios` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `id_servicio` INTEGER NOT NULL,
  `id_producto` INTEGER NOT NULL,
  `cantidad` INTEGER NOT NULL,
  `precio_venta_unitario` REAL NOT NULL,
  FOREIGN KEY (`id_servicio`) REFERENCES `servicios` (`id`),
  FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id`)
);

CREATE TABLE `permisos` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `nombre_permiso` TEXT NOT NULL UNIQUE,
  `descripcion` TEXT
);

CREATE TABLE `rol_permisos` (
  `id_rol` INTEGER NOT NULL,
  `id_permiso` INTEGER NOT NULL,
  PRIMARY KEY (`id_rol`,`id_permiso`),
  FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id`),
  FOREIGN KEY (`id_permiso`) REFERENCES `permisos` (`id`)
);

-- Datos Esenciales (Semilla)
INSERT INTO `categorias` (`nombre`) VALUES ('Componentes'), ('Periféricos'), ('Audio y Video'), ('Cables y Adaptadores'), ('Servicios');
INSERT INTO `roles` (`nombre_rol`) VALUES ('Administrador'), ('Vendedor'), ('Técnico');
INSERT INTO `usuarios` (`nombre_usuario`, `password_hash`, `id_rol`, `nombre_completo`) VALUES ('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 1, 'Administrador del Sistema');
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
INSERT INTO `rol_permisos` (`id_rol`, `id_permiso`) SELECT 1, id FROM permisos;
INSERT INTO `rol_permisos` (`id_rol`, `id_permiso`) SELECT 2, id FROM permisos WHERE nombre_permiso IN ('access_dashboard','access_sales','access_inventory','access_clients','access_purchases');
INSERT INTO `rol_permisos` (`id_rol`, `id_permiso`) SELECT 3, id FROM permisos WHERE nombre_permiso IN ('access_dashboard','access_inventory','access_clients','access_services');
