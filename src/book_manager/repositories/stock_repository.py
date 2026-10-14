
from abc import ABC, abstractmethod
from typing import Optional, List

from sqlalchemy import select

from book_manager.entities import Stock, Editorial, Genero, Libro
from book_manager.database.connection import ConexionDB
from book_manager.models.models import StockModelo


class IRepositorioStock(ABC):
    """Interfaz para repositorios del tipo Stock."""

    @abstractmethod
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

    @abstractmethod
    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        """Lee un registro de stock por ID de libro.

        Args:
            libro_id (int): El ID del libro asociado al stock.

        Returns:
            Optional[Stock]: El objeto Stock si se encuentra, None en caso
                contrario.
        """
        pass

    @abstractmethod
    def leer_todos(self) -> List[Stock]:
        """devuelve el stock de todos los libros."""
        pass

    @abstractmethod
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

    @abstractmethod
    def eliminar(self, libro_id: int) -> bool:
        """Elimina un registro de stock por ID de libro.

        Args:
            libro_id (int): El ID del libro asociado al stock a eliminar.

        Returns:
            bool: True si el stock fue eliminado, False si no se encontró.
        """
        pass

    


class RepositorioStock(IRepositorioStock):
    """Repositorio de stock guardado en CSV. La clave es el id del libro."""

    campos = ["libro_id", "cantidad", "cantidad_minima"]

    def __init__(self, conexion: ConexionDB) -> None:
        self._conexion = conexion

    def _a_entidad(
            self,
            modelo: StockModelo
    ) -> Stock:
        """Convierte un modelo de SQLAlchemy a una entidad de dominio."""
        libro_modelo = modelo.libro

        editorial = Editorial(
            libro_modelo.editorial.id,
            libro_modelo.editorial.nombre,
            libro_modelo.editorial.pais,
            libro_modelo.editorial.sitio_web
        )

        genero = Genero(
            libro_modelo.genero.id,
            libro_modelo.genero.nombre,
            libro_modelo.genero.descripcion
        )

        libro = Libro(
            libro_modelo.id,
            libro_modelo.isbn,
            libro_modelo.titulo,
            libro_modelo.autor,
            editorial,
            genero,
            libro_modelo.anio_publicacion
        )

        return Stock(
            libro,
            modelo.cantidad,
            modelo.cantidad_minima
        )

    def leer_por_libro(
            self,
            libro_id: int
            ) -> Optional[Stock]:
        """Lee un registro de stock por ID de libro."""

        with self._conexion.transaccion() as sesion: 
            modelo = sesion.get(StockModelo, libro_id)

            if modelo is None:
                return None

            return  self._a_entidad(modelo)

    def leer_todos(
            self
            ) -> List[Stock]:
        """Lee todos los registros de stock."""

        with self._conexion.transaccion() as sesion:
            query = select(StockModelo).order_by(StockModelo.libro_id)

            modelos = sesion.scalars(query).all()

            return [
                self._a_entidad(modelo)
                for modelo in modelos
            ]

    def crear(
            self, 
            stock: Stock
            ) -> Stock:
        """Crea un nuevo registro de stock."""

        with self._conexion.transaccion() as sesion:
            if sesion.get(StockModelo, stock.libro_id) is not None:
                raise ValueError(
                    f"Ya existe un registro de stock para el libro con id {stock.libro_id}"
                )

            modelo = StockModelo(
                libro_id=stock.libro_id,
                cantidad=stock.cantidad,
                cantidad_minima=stock.cantidad_minima
            )

            sesion.add(modelo)
            sesion.flush()  # Asegura que el modelo se guarde y se genere el ID

            return self._a_entidad(modelo)

    def actualizar(
            self,
            stock: Stock
            ) -> Stock:
        """Actualiza un registro de stock existente."""

        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(StockModelo, stock.libro_id)

            if modelo is None:
                raise ValueError(
                    f"No existe un registro de stock para el libro con id {stock.libro_id}"
                )

            modelo.cantidad = stock.cantidad
            modelo.cantidad_minima = stock.cantidad_minima
            sesion.flush()  # Asegura que los cambios se guarden

            return self._a_entidad(modelo
    )

    def eliminar(
            self,
            libro_id: int
            ) -> bool:
        """Elimina un registro de stock por ID de libro."""

        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(StockModelo, libro_id)

            if modelo is None:
                return False

            sesion.delete(modelo)

            return True
        
    