"""Configuración de los repositorios del sistema."""

from pathlib import Path

from book_manager.repositories.archivo_csv_repository import ArchivoCSV
from book_manager.database.connection import ConexionDB
from book_manager.repositories.editorial_repository import (
    RepositorioEditorial,
)
from book_manager.repositories.genero_repository import RepositorioGenero
from book_manager.repositories.moneda_repository import RepositorioMoneda
from book_manager.repositories.tipo_cotizacion_repository import (
    RepositorioTipoCotizacion,
)
from book_manager.repositories.libro_repository import RepositorioLibro
from book_manager.repositories.precio_repository import RepositorioPrecio
from book_manager.repositories.stock_repository import RepositorioStock
from book_manager.repositories.cotizacion_dolar_repository import (
    RepositorioCotizacionDolar,
)


DIRECTORIO_DATOS = (
    Path(__file__).resolve().parent.parent / "migrations" / "csv"
)


class Repositorios:
    """Crea los repositorios del sistema."""

    def __init__(
        self,
        conexion: ConexionDB,
        directorio: Path = DIRECTORIO_DATOS,
    ) -> None:
        """Inicializa los repositorios CSV y PostgreSQL."""

        self.generos = RepositorioGenero(directorio / "generos.csv")
        self.editoriales = RepositorioEditorial(
            directorio / "editoriales.csv"
        )
        self.monedas = RepositorioMoneda(directorio / "monedas.csv")

        self.tipos_cotizacion = RepositorioTipoCotizacion(conexion)

        self.libros = RepositorioLibro(
            directorio / "libros.csv",
            self.editoriales,
            self.generos,
        )
        self.precios = RepositorioPrecio(
            directorio / "precios.csv",
            self.libros,
            self.monedas,
        )
        self.stock = RepositorioStock(
            directorio / "stock.csv",
            self.libros,
        )

        self.cotizaciones = RepositorioCotizacionDolar(conexion)