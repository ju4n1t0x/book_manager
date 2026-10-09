
import abc, csv

from pathlib import Path
from typing import Iterator, List, Optional, TypeVar
from book_manager.entities import EntidadBase
from book_manager.repositories.irepositorio import IRepositorio


T = TypeVar("T", bound=EntidadBase)

class ArchivoCSV:
    """Lectura y escritura de un archivo CSV con encabezado."""

    def __init__(self, ruta: Path, campos: List[str]) -> None:
        self._ruta = ruta
        self._campos = campos

    def leer(self) -> Iterator[dict[str, str]]:
        """Devuelve las filas del archivo de a una.

        Returns:
            Iterator[dict[str, str]]: Cada fila como diccionario
                campo -> valor.
        """
        if not self._ruta.exists():
            return
        with open(self._ruta, "r", encoding="utf-8", newline="") as archivo:
            for fila in csv.DictReader(archivo):
                yield fila

    def escribir(self, filas: List[dict]) -> None:
        """Reescribe el archivo completo con las filas recibidas."""
        self._ruta.parent.mkdir(parents=True, exist_ok=True)
        with open(self._ruta, "w", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=self._campos)
            escritor.writeheader()
            escritor.writerows(filas)


class RepositorioCSV(IRepositorio[T]):
    """Repositorio genérico que guarda las entidades en un archivo CSV.

    Mantiene las entidades en memoria y reescribe el archivo en cada cambio.
    Cada repositorio concreto indica los campos del archivo y cómo pasar
    una entidad a una fila y viceversa.
    """

    campos: List[str] = []

    def __init__(self, ruta: Path) -> None:
        self._archivo = ArchivoCSV(ruta, self.campos)
        self._entidades: dict[int, T] = {}
        for fila in self._archivo.leer():
            entidad = self._desde_fila(fila)
            self._entidades[entidad.id] = entidad

    @abc.abstractmethod
    def _a_fila(self, entidad: T) -> dict:
        """Convierte la entidad en una fila del CSV."""

    @abc.abstractmethod
    def _desde_fila(self, fila: dict[str, str]) -> T:
        """Arma la entidad a partir de una fila del CSV."""

    def _guardar(self) -> None:
        self._archivo.escribir(
            [self._a_fila(e) for e in self._entidades.values()]
        )

    def _proximo_id(self) -> int:
        return max(self._entidades, default=0) + 1

    def crear(self, entidad: T) -> T:
        if entidad.id == 0:
            entidad.id = self._proximo_id()
        if entidad.id in self._entidades:
            raise ValueError(f"Ya existe un registro con id {entidad.id}.")
        self._entidades[entidad.id] = entidad
        self._guardar()
        return entidad

    def leer_por_id(self, id: int) -> Optional[T]:
        return self._entidades.get(id)

    def leer_todos(self) -> List[T]:
        return list(self._entidades.values())

    def actualizar(self, entidad: T) -> T:
        """Actualiza una entidad existente.

        Los datos nuevos se copian sobre el objeto que ya existe, así los
        objetos que lo referencian (por ejemplo un libro con su género) ven
        el cambio.
        """
        actual = self._entidades.get(entidad.id)
        if actual is None:
            raise ValueError(f"No existe un registro con id {entidad.id}.")
        if actual is not entidad:
            vars(actual).update(vars(entidad))
        self._guardar()
        return actual

    def eliminar(self, id: int) -> bool:
        if id not in self._entidades:
            return False
        del self._entidades[id]
        self._guardar()
        return True