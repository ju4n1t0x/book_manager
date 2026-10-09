
import abc

from typing import Optional, List
from pathlib import Path
from book_manager.entities import Stock

from book_manager.repositories.archivo_csv_repository import ArchivoCSV
from book_manager.repositories.libro_repository import RepositorioLibro

class IRepositorioStock(abc.ABC):
    """Interfaz para repositorios del tipo Stock."""

    @abc.abstractmethod
    def crear(self, stock: Stock) -> Stock:
        """Crea un nuevo registro de stock.

        Args:
            stock (Stock): El objeto Stock a crear.

        Returns:
            Stock: El objeto Stock creado.

        Raises:
            ValueError: Si ya existe un registro de stock para el mismo libro.
        """
        pass

    @abc.abstractmethod
    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        """Lee un registro de stock por ID de libro.

        Args:
            libro_id (int): El ID del libro asociado al stock.

        Returns:
            Optional[Stock]: El objeto Stock si se encuentra, None en caso
                contrario.
        """
        pass

    @abc.abstractmethod
    def actualizar(self, stock: Stock) -> Stock:
        """Actualiza un registro de stock existente.

        Args:
            stock (Stock): El objeto Stock a actualizar (debe tener un
                libro_id existente).

        Returns:
            Stock: El objeto Stock actualizado.

        Raises:
            ValueError: Si no se encuentra el stock para actualizar.
        """
        pass

    @abc.abstractmethod
    def eliminar(self, libro_id: int) -> bool:
        """Elimina un registro de stock por ID de libro.

        Args:
            libro_id (int): El ID del libro asociado al stock a eliminar.

        Returns:
            bool: True si el stock fue eliminado, False si no se encontró.
        """
        pass

    @abc.abstractmethod
    def leer_todos(self) -> List[Stock]:
        """devuelve el stock de todos los libros."""
        pass


class RepositorioStock(IRepositorioStock):
    """Repositorio de stock guardado en CSV. La clave es el id del libro."""

    campos = ["libro_id", "cantidad", "cantidad_minima"]

    def __init__(self, ruta: Path, libros: RepositorioLibro) -> None:
        self._libros = libros
        self._archivo = ArchivoCSV(ruta, self.campos)
        self._stock: dict[int, Stock] = {}
        for fila in self._archivo.leer():
            stock = self._desde_fila(fila)
            self._stock[stock.libro_id] = stock

    def _a_fila(self, stock: Stock) -> dict:
        return {
            "libro_id": stock.libro_id,
            "cantidad": stock.cantidad,
            "cantidad_minima": stock.cantidad_minima,
        }

    def _desde_fila(self, fila: dict[str, str]) -> Stock:
        libro = self._libros.leer_por_id(int(fila["libro_id"]))
        if libro is None:
            raise ValueError(
                f"Hay stock cargado para el libro {fila['libro_id']} "
                "que no existe."
            )
        return Stock(
            libro, int(fila["cantidad"]), int(fila["cantidad_minima"])
        )

    def _guardar(self) -> None:
        self._archivo.escribir([self._a_fila(s) for s in self._stock.values()])

    def crear(self, stock: Stock) -> Stock:
        if stock.libro_id in self._stock:
            raise ValueError(
                f"Ya hay stock cargado para el libro {stock.libro_id}."
            )
        self._stock[stock.libro_id] = stock
        self._guardar()
        return stock

    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        return self._stock.get(libro_id)

    def leer_todos(self) -> List[Stock]:
        """Devuelve el stock de todos los libros."""
        return list(self._stock.values())

    def actualizar(self, stock: Stock) -> Stock:
        if stock.libro_id not in self._stock:
            raise ValueError(
                f"No hay stock cargado para el libro {stock.libro_id}."
            )
        self._stock[stock.libro_id] = stock
        self._guardar()
        return stock

    def eliminar(self, libro_id: int) -> bool:
        if libro_id not in self._stock:
            return False
        del self._stock[libro_id]
        self._guardar()
        return True