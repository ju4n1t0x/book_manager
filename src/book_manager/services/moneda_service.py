
from book_manager.entities import Moneda, Precio
from book_manager.repositories import IRepositorio
from book_manager.services.crud_services import ServicioCrud
from typing import Optional

class MonedaService(ServicioCrud[Moneda]):
    """Lógica de las monedas."""

    entidad = "la moneda"

    def __init__(
        self, repositorio: IRepositorio[Moneda], precios: IRepositorio[Precio]
    ) -> None:
        super().__init__(repositorio)
        self._precios = precios

    def buscar_por_codigo(self, codigo: str) -> Optional[Moneda]:
        return next(
            (m for m in self.listar() if m.codigo == codigo.upper()), None
        )

    def _validar(self, entidad: Moneda) -> None:
        existente = self.buscar_por_codigo(entidad.codigo)
        if existente is not None and existente.id != entidad.id:
            raise ValueError(f"Ya existe la moneda {entidad.codigo}.")

    def _validar_eliminacion(self, id: int) -> None:
        if any(
            precio.moneda.id == id for precio in self._precios.leer_todos()
        ):
            raise ValueError(
                "No se puede eliminar una moneda que se usa en algún precio."
            )