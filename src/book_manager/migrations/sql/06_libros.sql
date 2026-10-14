-- Datos de la tabla libros
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id, anio_publicacion) VALUES (1, '9788468778938', 'Cien años de soledad', 'Gabriel García Márquez', 1, 1, 1967) ON CONFLICT DO NOTHING;
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id, anio_publicacion) VALUES (2, '9789878792170', 'Rayuela', 'Julio Cortázar', 2, 1, 1963) ON CONFLICT DO NOTHING;
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id, anio_publicacion) VALUES (3, '9788432180965', 'Ficciones', 'Jorge Luis Borges', 1, 2, 1944) ON CONFLICT DO NOTHING;
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id, anio_publicacion) VALUES (4, '9788469290811', 'El túnel', 'Ernesto Sabato', 3, 1, 1948) ON CONFLICT DO NOTHING;
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id, anio_publicacion) VALUES (5, '9789500339070', 'Harry Potter y la piedra filosofal', 'J. K. Rowling', 4, 4, 1997) ON CONFLICT DO NOTHING;
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id, anio_publicacion) VALUES (6, '9788437938349', 'El principito', 'Antoine de Saint-Exupéry', 4, 4, 1943) ON CONFLICT DO NOTHING;
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id, anio_publicacion) VALUES (7, '9788460174684', 'Sapiens. De animales a dioses', 'Yuval Noah Harari', 5, 3, 2011) ON CONFLICT DO NOTHING;
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id, anio_publicacion) VALUES (8, '9789504538400', 'Homo Deus', 'Yuval Noah Harari', 5, 3, 2015) ON CONFLICT DO NOTHING;
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id, anio_publicacion) VALUES (9, '9789509161467', 'Fluent Python', 'Luciano Ramalho', 6, 5, 2015) ON CONFLICT DO NOTHING;
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id, anio_publicacion) VALUES (10, '9789500033077', 'Learning Python', 'Mark Lutz', 6, 5, 2013) ON CONFLICT DO NOTHING;
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id, anio_publicacion) VALUES (11, '9788466619349', 'Bestiario', 'Julio Cortázar', 1, 2, 1951) ON CONFLICT DO NOTHING;
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id, anio_publicacion) VALUES (12, '9788431450618', 'Sobre héroes y tumbas', 'Ernesto Sabato', 3, 1, 1961) ON CONFLICT DO NOTHING;
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id, anio_publicacion) VALUES (13, '9780571394777', 'Ariel', 'Sylvia Plath', 10, 6, 1965) ON CONFLICT DO NOTHING;
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id, anio_publicacion) VALUES (14, '9788433941848', 'Sontag', 'Benjamin Moser', 8, 7, 2020) ON CONFLICT DO NOTHING;
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id, anio_publicacion) VALUES (15, '9788408074014', 'La increíble historia de la humanidad. De la Edad de Piedra a nuestros tiempos', 'James C. Davis', 7, 8, 2007) ON CONFLICT DO NOTHING;
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id, anio_publicacion) VALUES (16, '9780571360550', 'Being You', 'Anil Seth', 10, 9, 2021) ON CONFLICT DO NOTHING;
INSERT INTO libros (id, isbn, titulo, autor, editorial_id, genero_id, anio_publicacion) VALUES (17, '9783518293263', 'Geschichte der Moralphilosophie', 'John Rawls', 9, 10, 2004) ON CONFLICT DO NOTHING;
