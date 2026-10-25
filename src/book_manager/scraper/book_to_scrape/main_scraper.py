import os
import sys
from pathlib import Path

RUTA_SCRAPER = Path(__file__).resolve().parent
RUTA_SRC = Path(__file__).resolve().parents[3]
RUTA_ENV = RUTA_SRC / "book_manager" / ".env"

sys.path.insert(0, str(RUTA_SCRAPER))
sys.path.insert(0, str(RUTA_SRC))

from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from book_manager.database.connection import ConexionDB
from book_manager.repositories.repositories import Repositorios
from book_manager.services import DolarApi, Servicios
from book_to_scrape.spiders.cuspide_spider import CuspideSpider

def main():
    load_dotenv(RUTA_ENV)

    url = os.getenv("DIRECT_URL")

    if not url:
        raise ValueError("La variable de entorno 'DIRECT_URL' no está definida.")

    conexion = ConexionDB(url)

    libros_catalogo = []
    consultas_vistas = set()

    try:
        servicios = Servicios(Repositorios(conexion), DolarApi())
        for libro in servicios.libros.listar():
            clave = (libro.titulo.casefold(), libro.autor.casefold())

            if clave in consultas_vistas:
                continue

            consultas_vistas.add(clave)
            libros_catalogo.append({
                "titulo": libro.titulo,
                "autor": libro.autor
            })
    finally:
        conexion.close()

    if not libros_catalogo:
        raise ValueError("El catalogo no contiene libros para buscar")

    print(f"Se buscaran {len(libros_catalogo)} libros del catalogo en Cuspide.com")

    settings = Settings()
    settings.setmodule("book_to_scrape.settings", priority="project")


    process = CrawlerProcess(settings)
    process.crawl(CuspideSpider, libros=libros_catalogo)
    process.start()


if __name__ == "__main__":
    main()