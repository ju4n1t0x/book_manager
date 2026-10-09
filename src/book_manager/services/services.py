

from book_manager.services import (
    EditorialService,
    MonedaService,
    TipoCotizacionService,
    LibroService,
    PrecioService,
    StockService,
    ProveedorCotizaciones,
    CotizacionService,
    GeneroService,
    ReporteService,
    CotizadorService,
)
from book_manager.repositories import Repositorios

class Servicios:
    """Crea todos los servicios a partir de los repositorios."""

    def __init__(
        self, repositorios: Repositorios, proveedor: ProveedorCotizaciones
    ) -> None:
        self.generos = GeneroService(repositorios.generos, repositorios.libros)
        self.editoriales = EditorialService(
            repositorios.editoriales, repositorios.libros
        )
        self.monedas = MonedaService(
            repositorios.monedas, repositorios.precios
        )
        self.tipos_cotizacion = TipoCotizacionService(
            repositorios.tipos_cotizacion, repositorios.cotizaciones
        )
        self.libros = LibroService(
            repositorios.libros, repositorios.precios, repositorios.stock
        )
        self.precios = PrecioService(repositorios.precios)
        self.stock = StockService(repositorios.stock, repositorios.libros)
        self.cotizaciones = CotizacionService(
            repositorios.cotizaciones, self.tipos_cotizacion, proveedor
        )
        self.cotizador = CotizadorService(
            self.precios, self.cotizaciones, self.tipos_cotizacion
        )
        self.reportes = ReporteService(self.libros, self.stock, self.cotizador)
