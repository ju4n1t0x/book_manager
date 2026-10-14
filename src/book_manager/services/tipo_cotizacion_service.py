
from typing import Optional


from book_manager.entities import TipoCotizacion
from book_manager.repositories import IRepositorio, IRepositorioCotizacionDolar
from book_manager.services.crud_services import ServicioCrud

class TipoCotizacionService(ServicioCrud[TipoCotizacion]):
    """Lógica de los tipos de cotización."""

    entidad = "el tipo de cotización"

    def __init__(
        self,
        repositorio: IRepositorio[TipoCotizacion],
        cotizaciones: IRepositorioCotizacionDolar,
    ) -> None:
        super().__init__(repositorio)
        self._cotizaciones = cotizaciones

    def buscar_por_codigo(self, codigo: str) -> Optional[TipoCotizacion]:
        return next(
            (t for t in self.listar() if t.codigo == codigo.lower()), None
        )

    def _validar(self, entidad: TipoCotizacion) -> None:
        existente = self.buscar_por_codigo(entidad.codigo)
        if existente is not None and existente.id != entidad.id:
            raise ValueError(
                f"Ya existe el tipo de cotización con código {entidad.codigo}."
            )

    def _validar_eliminacion(self, id: int) -> None:
        if self._cotizaciones.leer_historico_por_tipo(id):
            raise ValueError(
                "No se puede eliminar un tipo que tiene cotizaciones cargadas."
            )