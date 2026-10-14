-- Datos de la tabla editoriales
INSERT INTO editoriales (id, nombre, pais, sitio_web) VALUES (1, 'Sudamericana', 'Argentina', 'https://www.penguinlibros.com') ON CONFLICT DO NOTHING;
INSERT INTO editoriales (id, nombre, pais, sitio_web) VALUES (2, 'Alfaguara', 'España', 'https://www.penguinlibros.com') ON CONFLICT DO NOTHING;
INSERT INTO editoriales (id, nombre, pais, sitio_web) VALUES (3, 'Seix Barral', 'España', 'https://www.planetadelibros.com') ON CONFLICT DO NOTHING;
INSERT INTO editoriales (id, nombre, pais, sitio_web) VALUES (4, 'Salamandra', 'España', 'https://www.penguinlibros.com') ON CONFLICT DO NOTHING;
INSERT INTO editoriales (id, nombre, pais, sitio_web) VALUES (5, 'Debate', 'España', 'https://www.penguinlibros.com') ON CONFLICT DO NOTHING;
INSERT INTO editoriales (id, nombre, pais, sitio_web) VALUES (6, 'O''Reilly Media', 'Estados Unidos', 'https://www.oreilly.com') ON CONFLICT DO NOTHING;
INSERT INTO editoriales (id, nombre, pais, sitio_web) VALUES (7, 'Planeta', 'España', 'https://planeta.es') ON CONFLICT DO NOTHING;
INSERT INTO editoriales (id, nombre, pais, sitio_web) VALUES (8, 'Anagrama', 'España', 'https://www.anagrama-ed.es') ON CONFLICT DO NOTHING;
INSERT INTO editoriales (id, nombre, pais, sitio_web) VALUES (9, 'Suhrkamp Verlag', 'Alemania', 'https://www.suhrkamp.de') ON CONFLICT DO NOTHING;
INSERT INTO editoriales (id, nombre, pais, sitio_web) VALUES (10, 'Faber & Faber', 'Reino Unido', 'https://www.faber.co.uk') ON CONFLICT DO NOTHING;
