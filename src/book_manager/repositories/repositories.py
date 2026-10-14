"""Configuración de los repositorios del sistema."""

from pathlib import Path

from book_manager.database.connection import ConexionDB
from book_manager.repositories.editorial_repository import (
    RepositorioEditorial,
)
from book_manager.repositories.genero_repository import RepositorioGenero
from book_manager.repositories.tipo_cotizacion_repository import (
    RepositorioTipoCotizacion,
)
from book_manager.repositories.libro_repository import RepositorioLibro
from book_manager.repositories.moneda_repository import RepositorioMoneda
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
    ) -> None:
        """Inicializa los repositorios CSV y PostgreSQL."""

        self.generos = RepositorioGenero(conexion)
        self.editoriales = RepositorioEditorial(conexion)
        self.monedas = RepositorioMoneda(conexion)
        self.tipos_cotizacion = RepositorioTipoCotizacion(conexion)
        self.libros = RepositorioLibro(conexion)
        self.precios = RepositorioPrecio(conexion)
        self.stock = RepositorioStock(conexion)
        self.cotizaciones = RepositorioCotizacionDolar(conexion)
