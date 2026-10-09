
from pathlib import Path
from typing import List

from book_manager.repositories.archivo_csv_repository import RepositorioCSV
from book_manager.repositories.moneda_repository import RepositorioMoneda
from book_manager.repositories.libro_repository import RepositorioLibro

from book_manager.entities import (
    Precio,
)


class RepositorioPrecio(RepositorioCSV[Precio]):
    """Repositorio de precios."""

    campos = ["id", "libro_id", "moneda_id", "monto"]

    def __init__(
        self, ruta: Path, libros: RepositorioLibro, monedas: RepositorioMoneda
    ) -> None:
        self._libros = libros
        self._monedas = monedas
        super().__init__(ruta)

    def _a_fila(self, entidad: Precio) -> dict:
        return {
            "id": entidad.id,
            "libro_id": entidad.libro.id,
            "moneda_id": entidad.moneda.id,
            "monto": entidad.monto,
        }

    def _desde_fila(self, fila: dict[str, str]) -> Precio:
        libro = self._libros.leer_por_id(int(fila["libro_id"]))
        moneda = self._monedas.leer_por_id(int(fila["moneda_id"]))
        if libro is None or moneda is None:
            raise ValueError(
                f"El precio {fila['id']} tiene un libro o una moneda "
                "que no existe."
            )
        return Precio(int(fila["id"]), libro, moneda, float(fila["monto"]))

    def leer_por_libro(self, libro_id: int) -> List[Precio]:
        """Devuelve los precios cargados para un libro."""
        return [p for p in self._entidades.values() if p.libro.id == libro_id]