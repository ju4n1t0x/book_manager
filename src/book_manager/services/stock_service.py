
from typing import List
from book_manager.entities import Stock, Libro
from book_manager.repositories import IRepositorio, IRepositorioStock
from book_manager.services.auditoria import auditar

class StockService:
    """Lógica del stock de los libros."""

    def __init__(
        self, repositorio: IRepositorioStock, libros: IRepositorio[Libro]
    ) -> None:
        self._repositorio = repositorio
        self._libros = libros


    @auditar("listar_stock")
    def listar(self) -> List[Stock]:
        return self._repositorio.leer_todos()

    @auditar("buscar_stock")
    def buscar(self, libro_id: int) -> Stock:
        """Devuelve el stock de un libro.

        Raises:
            ValueError: Si el libro no tiene stock cargado.
        """
        stock = self._repositorio.leer_por_libro(libro_id)
        if stock is None:
            raise ValueError(f"El libro {libro_id} no tiene stock cargado.")
        return stock

    @auditar("crear_stock")
    def crear(
        self, libro_id: int, cantidad: int, cantidad_minima: int
    ) -> Stock:
        libro = self._libros.leer_por_id(libro_id)
        if libro is None:
            raise ValueError(f"No existe un libro con id {libro_id}.")
        return self._repositorio.crear(Stock(libro, cantidad, cantidad_minima))

    @auditar("actualizar_stock")
    def actualizar(
        self, libro_id: int, cantidad: int, cantidad_minima: int
    ) -> Stock:
        stock = self.buscar(libro_id)
        nuevo = Stock(stock.libro, cantidad, cantidad_minima)
        return self._repositorio.actualizar(nuevo)

    @auditar("eliminar_stock")
    def eliminar(self, libro_id: int) -> None:
        if not self._repositorio.eliminar(libro_id):
            raise ValueError(f"El libro {libro_id} no tiene stock cargado.")

    @auditar("reponer_stock")
    def reponer(self, libro_id: int, cantidad: int) -> Stock:
        """Suma unidades al stock de un libro, por ejemplo por un pedido.

        Args:
            libro_id (int): Id del libro.
            cantidad (int): Unidades que ingresan, debe ser mayor a cero.

        Returns:
            Stock: El stock actualizado.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad a reponer debe ser mayor a cero.")
        stock = self.buscar(libro_id)
        nuevo = Stock(
            stock.libro, stock.cantidad + cantidad, stock.cantidad_minima
        )
        return self._repositorio.actualizar(nuevo)

    @auditar("descontar_stock")
    def descontar(self, libro_id: int, cantidad: int) -> Stock:
        """Resta unidades del stock de un libro (por ejemplo por una venta).

        Args:
            libro_id (int): Id del libro.
            cantidad (int): Unidades que salen, debe ser mayor a cero.

        Returns:
            Stock: El stock actualizado.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad a descontar debe ser mayor a cero.")
        stock = self.buscar(libro_id)
        if cantidad > stock.cantidad:
            raise ValueError(
                f"No hay suficiente stock del libro {libro_id}: "
                f"hay {stock.cantidad} y se quieren descontar {cantidad}."
            )
        nuevo = Stock(
            stock.libro, stock.cantidad - cantidad, stock.cantidad_minima
        )
        return self._repositorio.actualizar(nuevo)