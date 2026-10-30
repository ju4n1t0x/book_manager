
from typing import List
from book_manager.entities import Precio
from book_manager.repositories import RepositorioPrecio
from book_manager.services.crud_services import ServicioCrud

class PrecioService(ServicioCrud[Precio]):
    """Lógica de los precios.

    Un libro tiene como máximo un precio por moneda.
    """

    entidad = "el precio"

    def __init__(self, repositorio: RepositorioPrecio) -> None:
        super().__init__(repositorio)
        self._precios = repositorio

    def precios_de_libro(self, libro_id: int) -> List[Precio]:
        return self._precios.leer_por_libro(libro_id)

    def _validar(self, entidad: Precio) -> None:
        for precio in self.precios_de_libro(entidad.libro.id):
            if (
                precio.id != entidad.id
                and precio.moneda.id == entidad.moneda.id
            ):
                raise ValueError(
                    "El libro ya tiene un precio en "
                    f"{entidad.moneda.codigo}, modificá ese."
                )