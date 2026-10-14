-- Datos de la tabla monedas
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (1, 'ARS', 'Peso argentino', '$') ON CONFLICT DO NOTHING;
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (2, 'USD', 'Dólar estadounidense', 'US$') ON CONFLICT DO NOTHING;
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (3, 'BRL', 'Real brasileño', 'R$') ON CONFLICT DO NOTHING;
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (4, 'CLP', 'Peso chileno', '$') ON CONFLICT DO NOTHING;
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (5, 'UYU', 'Peso uruguayo', '$U') ON CONFLICT DO NOTHING;
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (6, 'MXN', 'Peso mexicano', 'MEX$') ON CONFLICT DO NOTHING;
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (7, 'EUR', 'Euro', '€') ON CONFLICT DO NOTHING;
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (8, 'GBP', 'Libra esterlina', '£') ON CONFLICT DO NOTHING;
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (9, 'JPY', 'Yen japonés', '¥') ON CONFLICT DO NOTHING;
INSERT INTO monedas (id, codigo, nombre, simbolo) VALUES (10, 'CAD', 'Dólar canadiense', 'C$') ON CONFLICT DO NOTHING;
