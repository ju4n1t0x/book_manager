import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

RUTA_SCRAPER = Path(__file__).resolve().parent
RUTA_SRC = Path(__file__).resolve().parents[3]
RUTA_ENV = RUTA_SRC / "book_manager" / ".env"
RUTA_REPORTES = RUTA_SRC / "book_manager" / "reportes"

sys.path.insert(0, str(RUTA_SCRAPER))
sys.path.insert(0, str(RUTA_SRC))

from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from book_manager.database.connection import ConexionDB
from book_manager.repositories.repositories import Repositorios
from book_manager.services import DolarApi, Servicios
from book_manager.services.alerta_precio_service import AlertaPrecioService
from book_manager.ui.console import pedir_decimal, pedir_entero
from book_to_scrape.spiders.cuspide_spider import CuspideSpider


def pedir_diferencia_minima() -> float:
    """Pide al usuario la diferencia de precio que dispara una alerta."""
    while True:
        diferencia = pedir_decimal(
            "Diferencia mínima de precio, en pesos, para generar alerta"
        )
        if diferencia >= 0:
            return diferencia
        print("La diferencia no puede ser negativa.")


def pedir_tipo_cotizacion(servicios: Servicios) -> int:
    """Pide el tipo de dólar con el que se pasan a pesos los precios en USD."""
    tipos = servicios.tipos_cotizacion.listar()
    if not tipos:
        raise ValueError("No hay tipos de cotización cargados.")

    print("\nTipos de cotización disponibles:")
    for tipo in tipos:
        print(f"  {tipo.id}. {tipo}")

    ids = {tipo.id for tipo in tipos}
    while True:
        elegido = pedir_entero("Id del tipo de cotización a usar")
        if elegido in ids:
            return elegido
        print("Elegí uno de los ids de la lista.")


def obtener_libros_catalogo(servicios: Servicios) -> List[Dict[str, str]]:
    """Devuelve los libros del catálogo sin repetir título y autor."""
    libros_catalogo = []
    consultas_vistas = set()

    for libro in servicios.libros.listar():
        clave = (libro.titulo.casefold(), libro.autor.casefold())

        if clave in consultas_vistas:
            continue

        consultas_vistas.add(clave)
        libros_catalogo.append({
            "titulo": libro.titulo,
            "autor": libro.autor
        })

    return libros_catalogo


def generar_alertas(
    url: str,
    ruta_resultados: Path,
    diferencia_minima: float,
    tipo_cotizacion_id: int,
) -> Path:
    """Compara los precios y genera el csv de alertas.

    Args:
        url (str): Url de conexión a la base de datos.
        ruta_resultados (Path): Csv que dejó el scraper.
        diferencia_minima (float): Diferencia mínima, en pesos, ingresada
            por el usuario.
        tipo_cotizacion_id (int): Tipo de dólar usado para convertir.

    Returns:
        Path: Ruta del csv de alertas generado.
    """
    conexion = ConexionDB(url)
    try:
        servicios = Servicios(Repositorios(conexion), DolarApi())
        alertas = AlertaPrecioService(servicios.libros, servicios.cotizador)
        ruta, cantidad = alertas.generar(
            ruta_resultados,
            RUTA_REPORTES,
            diferencia_minima,
            tipo_cotizacion_id,
        )
    finally:
        conexion.close()

    print(f"\nSe generaron {cantidad} alertas de precio.")
    print(f"Archivo de alertas: {ruta}")
    return ruta


def main(
    diferencia_minima: Optional[float] = None,
    tipo_cotizacion_id: Optional[int] = None,
) -> Path:
    """Ejecuta el scraper y genera el csv de alertas de precios.

    Si no se reciben la diferencia mínima o el tipo de cotización, se los
    pide al usuario antes de ejecutar el scraper.

    Args:
        diferencia_minima (Optional[float]): Diferencia mínima, en pesos,
            para generar una alerta.
        tipo_cotizacion_id (Optional[int]): Tipo de dólar usado para pasar
            a pesos los precios en dólares.

    Returns:
        Path: Ruta del csv de alertas generado.
    """
    load_dotenv(RUTA_ENV)

    url = os.getenv("DIRECT_URL")

    if not url:
        raise ValueError("La variable de entorno 'DIRECT_URL' no está definida.")

    conexion = ConexionDB(url)

    try:
        servicios = Servicios(Repositorios(conexion), DolarApi())
        libros_catalogo = obtener_libros_catalogo(servicios)

        if not libros_catalogo:
            raise ValueError("El catalogo no contiene libros para buscar")

        if diferencia_minima is None:
            diferencia_minima = pedir_diferencia_minima()
        if tipo_cotizacion_id is None:
            tipo_cotizacion_id = pedir_tipo_cotizacion(servicios)
    finally:
        conexion.close()

    print(f"Se buscaran {len(libros_catalogo)} libros del catalogo en Cuspide.com")

    settings = Settings()
    settings.setmodule("book_to_scrape.settings", priority="project")

    process = CrawlerProcess(settings)
    process.crawl(CuspideSpider, libros=libros_catalogo)
    process.start()

    ruta_resultados = Path(
        settings.get("RUTA_ARCHIVO", RUTA_REPORTES / "cuspide_resultados.csv")
    )
    return generar_alertas(
        url, ruta_resultados, diferencia_minima, tipo_cotizacion_id
    )


if __name__ == "__main__":
    main()