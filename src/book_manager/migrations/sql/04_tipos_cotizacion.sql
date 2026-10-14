-- Datos de la tabla tipos_cotizacion
INSERT INTO tipos_cotizacion (id, codigo, nombre) VALUES (1, 'oficial', 'Oficial') ON CONFLICT DO NOTHING;
INSERT INTO tipos_cotizacion (id, codigo, nombre) VALUES (2, 'blue', 'Blue') ON CONFLICT DO NOTHING;
INSERT INTO tipos_cotizacion (id, codigo, nombre) VALUES (3, 'bolsa', 'MEP') ON CONFLICT DO NOTHING;
INSERT INTO tipos_cotizacion (id, codigo, nombre) VALUES (4, 'contadoconliqui', 'Contado con liquidación') ON CONFLICT DO NOTHING;
INSERT INTO tipos_cotizacion (id, codigo, nombre) VALUES (5, 'mayorista', 'Mayorista') ON CONFLICT DO NOTHING;
INSERT INTO tipos_cotizacion (id, codigo, nombre) VALUES (6, 'cripto', 'Cripto') ON CONFLICT DO NOTHING;
INSERT INTO tipos_cotizacion (id, codigo, nombre) VALUES (7, 'tarjeta', 'Tarjeta') ON CONFLICT DO NOTHING;
INSERT INTO tipos_cotizacion (id, codigo, nombre) VALUES (8, 'solidario', 'Solidario') ON CONFLICT DO NOTHING;
INSERT INTO tipos_cotizacion (id, codigo, nombre) VALUES (9, 'turista', 'Turista') ON CONFLICT DO NOTHING;
INSERT INTO tipos_cotizacion (id, codigo, nombre) VALUES (10, 'ahorro', 'Ahorro') ON CONFLICT DO NOTHING;
