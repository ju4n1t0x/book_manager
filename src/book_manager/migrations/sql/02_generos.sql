-- Datos de la tabla generos
INSERT INTO generos (id, nombre, descripcion) VALUES (1, 'Novela', 'Narrativa extensa de ficción') ON CONFLICT DO NOTHING;
INSERT INTO generos (id, nombre, descripcion) VALUES (2, 'Cuento', 'Relatos breves de ficción') ON CONFLICT DO NOTHING;
INSERT INTO generos (id, nombre, descripcion) VALUES (3, 'Ensayo', 'Textos de análisis y divulgación') ON CONFLICT DO NOTHING;
INSERT INTO generos (id, nombre, descripcion) VALUES (4, 'Infantil', 'Libros para chicos y juveniles') ON CONFLICT DO NOTHING;
INSERT INTO generos (id, nombre, descripcion) VALUES (5, 'Técnico', 'Informática y programación') ON CONFLICT DO NOTHING;
INSERT INTO generos (id, nombre, descripcion) VALUES (6, 'Poesía', 'Obras literarias escritas en verso') ON CONFLICT DO NOTHING;
INSERT INTO generos (id, nombre, descripcion) VALUES (7, 'Biografía', 'Relatos sobre la vida de una persona') ON CONFLICT DO NOTHING;
INSERT INTO generos (id, nombre, descripcion) VALUES (8, 'Historia', 'Obras sobre acontecimientos y procesos históricos') ON CONFLICT DO NOTHING;
INSERT INTO generos (id, nombre, descripcion) VALUES (9, 'Ciencia', 'Libros sobre conocimientos y divulgación científica') ON CONFLICT DO NOTHING;
INSERT INTO generos (id, nombre, descripcion) VALUES (10, 'Filosofía', 'Obras sobre pensamiento, ideas y cuestiones filosóficas') ON CONFLICT DO NOTHING;
