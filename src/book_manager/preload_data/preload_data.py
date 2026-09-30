"""Datos iniciales del sistema y su escritura en la carpeta migrations/csv."""

from pathlib import Path

from book_manager.repositories.repositories import (
    DIRECTORIO_DATOS,
    ArchivoCSV,
    RepositorioCotizacionDolar,
    RepositorioEditorial,
    RepositorioGenero,
    RepositorioLibro,
    RepositorioMoneda,
    RepositorioPrecio,
    RepositorioStock,
    RepositorioTipoCotizacion,
)

GENEROS = [
    (1, "Novela", "Narrativa extensa de ficción"),
    (2, "Cuento", "Relatos breves de ficción"),
    (3, "Ensayo", "Textos de análisis y divulgación"),
    (4, "Infantil", "Libros para chicos y juveniles"),
    (5, "Técnico", "Informática y programación"),
    (6, "Poesía", "Obras literarias escritas en verso"),
    (7, "Biografía", "Relatos sobre la vida de una persona"),
    (8, "Historia", "Obras sobre acontecimientos y procesos históricos"),
    (9, "Ciencia", "Libros sobre conocimientos y divulgación científica"),
    (10, "Filosofía", "Obras sobre pensamiento, ideas y cuestiones filosóficas"),
]

EDITORIALES = [
    (1, "Sudamericana", "Argentina", "https://www.penguinlibros.com"),
    (2, "Alfaguara", "España", "https://www.penguinlibros.com"),
    (3, "Seix Barral", "España", "https://www.planetadelibros.com"),
    (4, "Salamandra", "España", "https://www.penguinlibros.com"),
    (5, "Debate", "España", "https://www.penguinlibros.com"),
    (6, "O'Reilly Media", "Estados Unidos", "https://www.oreilly.com"),
    (7, "Planeta", "España", "https://planeta.es"),
    (8, "Anagrama", "España", "https://www.anagrama-ed.es"),
    (9, "Suhrkamp Verlag", "Alemania", "https://www.suhrkamp.de"),
    (10, "Faber & Faber", "Reino Unido", "https://www.faber.co.uk"),
]

MONEDAS = [
    (1, "ARS", "Peso argentino", "$"),
    (2, "USD", "Dólar estadounidense", "US$"),
    (3, "BRL", "Real brasileño", "R$"),
    (4, "CLP", "Peso chileno", "$"),
    (5, "UYU", "Peso uruguayo", "$U"),
    (6, "MXN", "Peso mexicano", "MEX$"),
    (7, "EUR", "Euro", "€"),
    (8, "GBP", "Libra esterlina", "£"),
    (9, "JPY", "Yen japonés", "¥"),
    (10, "CAD", "Dólar canadiense", "C$"),
]

# El código es el mismo que usa DolarApi para cada tipo de dólar
TIPOS_COTIZACION = [
    (1, "oficial", "Oficial"),
    (2, "blue", "Blue"),
    (3, "bolsa", "MEP"),
    (4, "contadoconliqui", "Contado con liquidación"),
    (5, "mayorista", "Mayorista"),
    (6, "cripto", "Cripto"),
    (7, "tarjeta", "Tarjeta"),
    (8, "solidario", "Solidario"),
    (9, "turista", "Turista"),
    (10, "ahorro", "Ahorro"),
]

# id, isbn, título, autor, editorial_id, genero_id, año
LIBROS = [
    (1, "9788468778938", "Cien años de soledad", "Gabriel García Márquez", 1, 1, 1967),
    (2, "9789878792170", "Rayuela", "Julio Cortázar", 2, 1, 1963),
    (3, "9788432180965", "Ficciones", "Jorge Luis Borges", 1, 2, 1944),
    (4, "9788469290811", "El túnel", "Ernesto Sabato", 3, 1, 1948),
    (5, "9789500339070", "Harry Potter y la piedra filosofal", "J. K. Rowling", 4, 4, 1997),
    (6, "9788437938349", "El principito", "Antoine de Saint-Exupéry", 4, 4, 1943),
    (7, "9788460174684", "Sapiens. De animales a dioses", "Yuval Noah Harari", 5, 3, 2011),
    (8, "9789504538400", "Homo Deus", "Yuval Noah Harari", 5, 3, 2015),
    (9, "9789509161467", "Fluent Python", "Luciano Ramalho", 6, 5, 2015),
    (10, "9789500033077", "Learning Python", "Mark Lutz", 6, 5, 2013),
    (11, "9788466619349", "Bestiario", "Julio Cortázar", 1, 2, 1951),
    (12, "9788431450618", "Sobre héroes y tumbas", "Ernesto Sabato", 3, 1, 1961),
    (13, "9780571394777", "Ariel", "Sylvia Plath", 10, 6, 1965),
    (14, "9788433941848", "Sontag", "Benjamin Moser", 8, 7, 2020),
    (
        15,
        "9788408074014",
        "La increíble historia de la humanidad. De la Edad de Piedra a nuestros tiempos",
        "James C. Davis",
        7,
        8,
        2007,
    ),
    (16, "9780571360550", "Being You", "Anil Seth", 10, 9, 2021),
    (17, "9783518293263", "Geschichte der Moralphilosophie", "John Rawls", 9, 10, 2004),
]

# id, libro_id, moneda_id, monto (1 = ARS, 2 = USD)
PRECIOS = [
    (1, 1, 1, 32900),
    (2, 2, 1, 28500),
    (3, 3, 1, 24900),
    (4, 4, 1, 19900),
    (5, 5, 2, 24.9),
    (6, 6, 1, 15900),
    (7, 7, 2, 29.5),
    (8, 8, 1, 34900),
    (9, 9, 2, 64.99),
    (10, 10, 2, 72.5),
    (11, 11, 1, 21500),
    (12, 12, 1, 31200),
    (13, 13, 2, 24.9),
    (14, 14, 2, 17.5),
    (15, 15, 2, 21.9),
    (16, 16, 2, 20.5),
    (17, 17, 2, 18.9),
]

# libro_id, cantidad, cantidad_minima
STOCK = [
    (1, 14, 5),
    (2, 3, 5),
    (3, 8, 4),
    (4, 2, 3),
    (5, 20, 6),
    (6, 11, 5),
    (7, 5, 5),
    (8, 7, 3),
    (9, 1, 2),
    (10, 0, 2),
    (11, 6, 3),
    (12, 4, 3),
    (13, 6, 3),
    (14, 9, 3),
    (15, 4, 2),
    (16, 7, 3),
    (17, 3, 2),
]

# tipo_id, fecha, compra, venta (valores reales tomados de api.argentinadatos.com)
COTIZACIONES = [
    (1, "2026-09-23", 1485, 1535),
    (1, "2026-09-24", 1485, 1535),
    (1, "2026-09-25", 1490, 1540),
    (2, "2026-09-23", 1535, 1555),
    (2, "2026-09-24", 1540, 1560),
    (2, "2026-09-25", 1540, 1560),
    (3, "2026-09-23", 1530.4, 1536.6),
    (3, "2026-09-24", 1537.6, 1542.9),
    (3, "2026-09-25", 1539, 1545.6),
    (4, "2026-09-23", 1594.6, 1598.3),
    (4, "2026-09-24", 1605.8, 1607.1),
    (4, "2026-09-25", 1612.5, 1614.3),
    (5, "2026-09-23", 1506, 1515),
    (5, "2026-09-24", 1507, 1516),
    (5, "2026-09-25", 1510, 1519),
    (6, "2026-09-23", 1589.48, 1593.58),
    (6, "2026-09-24", 1600.57, 1604.45),
    (6, "2026-09-25", 1605.68, 1610.04),
    (7, "2026-09-23", 1930.5, 1995.5),
    (7, "2026-09-24", 1930.5, 1995.5),
    (7, "2026-09-25", 1937, 2002),
]

# Nombre del archivo, columnas y registros de cada entidad
ARCHIVOS = [
    ("generos", RepositorioGenero.campos, GENEROS),
    ("editoriales", RepositorioEditorial.campos, EDITORIALES),
    ("monedas", RepositorioMoneda.campos, MONEDAS),
    ("tipos_cotizacion", RepositorioTipoCotizacion.campos, TIPOS_COTIZACION),
    ("libros", RepositorioLibro.campos, LIBROS),
    ("precios", RepositorioPrecio.campos, PRECIOS),
    ("stock", RepositorioStock.campos, STOCK),
    ("cotizaciones", RepositorioCotizacionDolar.campos, COTIZACIONES),
]


def cargar_datos_iniciales(directorio: Path = DIRECTORIO_DATOS) -> dict[str, int]:
    """Escribe los datos iniciales en los archivos CSV de migrations/csv.

    Los datos que había en esos archivos se reemplazan.

    Args:
        directorio (Path): Carpeta donde se escriben los archivos.

    Returns:
        dict[str, int]: Cantidad de registros escritos por archivo.
    """
    escritos = {}
    for nombre, campos, registros in ARCHIVOS:
        filas = [dict(zip(campos, registro)) for registro in registros]
        ArchivoCSV(directorio / f"{nombre}.csv", campos).escribir(filas)
        escritos[nombre] = len(filas)
    return escritos
