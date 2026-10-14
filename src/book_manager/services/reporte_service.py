
from typing import List, Optional
from book_manager.entities import Libro, Stock
from book_manager.services.libro_service import LibroService
from book_manager.services.stock_service import StockService
from book_manager.services.cotizacion_service import CotizadorService


class ReporteService:
    """Reportes del sistema."""

    def __init__(
        self,
        libros: LibroService,
        stock: StockService,
        cotizador: CotizadorService,
    ) -> None:
        self._libros = libros
        self._stock = stock
        self._cotizador = cotizador

    def catalogo_en_pesos(
        self, tipo_id: int
    ) -> List[tuple[Libro, Optional[float]]]:
        """Lista los libros con su precio en pesos según un tipo de dólar."""
        return [
            (libro, self._cotizador.precio_en_pesos(libro.id, tipo_id))
            for libro in self._libros.listar()
        ]

    def stock_bajo(self) -> List[Stock]:
        """Devuelve los libros cuya cantidad está en el mínimo o por debajo.

        Returns:
            List[Stock]: Registros de stock con cantidad <= cantidad_minima,
            ordenados de menor a mayor cantidad.
        """
        bajos = [
            stock
            for stock in self._stock.listar()
            if stock.cantidad <= stock.cantidad_minima
        ]
        return sorted(bajos, key=lambda stock: stock.cantidad)