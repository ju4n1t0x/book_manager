
import datetime
from typing import Generic, List, TypeVar
from book_manager.entities import EntidadBase


from book_manager.repositories import (
    IRepositorio,
)

T = TypeVar("T", bound=EntidadBase)


class ServicioCrud(Generic[T]):
    """Operaciones CRUD comunes a todas las entidades con id.

    Las subclases agregan sus validaciones redefiniendo _validar y
    _validar_eliminacion.
    """

    entidad = "el registro"

    def __init__(self, repositorio: IRepositorio[T]) -> None:
        self._repositorio = repositorio

    def listar(self) -> List[T]:
        return self._repositorio.leer_todos()

    def buscar(self, id: int) -> T:
        """Busca una entidad por id.

        Raises:
            ValueError: Si no existe.
        """
        entidad = self._repositorio.leer_por_id(id)
        if entidad is None:
            raise ValueError(f"No se encontró {self.entidad} con id {id}.")
        return entidad

    def crear(self, entidad: T) -> T:
        self._validar(entidad)
        return self._repositorio.crear(entidad)

    def actualizar(self, entidad: T) -> T:
        self.buscar(entidad.id)
        self._validar(entidad)
        return self._repositorio.actualizar(entidad)

    def eliminar(self, id: int) -> None:
        self.buscar(id)
        self._validar_eliminacion(id)
        self._repositorio.eliminar(id)

    def _validar(self, entidad: T) -> None:
        """Validaciones de negocio antes de crear o actualizar."""

    def _validar_eliminacion(self, id: int) -> None:
        """Validaciones de negocio antes de eliminar."""
