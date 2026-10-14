
from book_manager.entities import Libro
from book_manager.repositories import IRepositorio, RepositorioPrecio, IRepositorioStock
from book_manager.services.crud_services import ServicioCrud
from typing import List

class LibroService(ServicioCrud[Libro]):
    """Lógica de los libros."""

    entidad = "el libro"

    def __init__(
        self,
        repositorio: IRepositorio[Libro],
        precios: RepositorioPrecio,
        stock: IRepositorioStock,
    ) -> None:
        super().__init__(repositorio)
        self._precios = precios
        self._stock = stock

    def buscar_por_titulo(self, texto: str) -> List[Libro]:
        texto = texto.lower()
        return [
            libro for libro in self.listar() if texto in libro.titulo.lower()
        ]

    def _validar(self, entidad: Libro) -> None:
        for libro in self.listar():
            if libro.id != entidad.id and libro.isbn == entidad.isbn:
                raise ValueError(
                    f"Ya existe un libro con el ISBN {entidad.isbn}."
                )

    def eliminar(self, id: int) -> None:
        """Elimina el libro junto con sus precios y su stock."""
        self.buscar(id)
        for precio in self._precios.leer_por_libro(id):
            self._precios.eliminar(precio.id)
        self._stock.eliminar(id)
        self._repositorio.eliminar(id)