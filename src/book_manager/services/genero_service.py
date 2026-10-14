
from book_manager.entities import Genero, Libro
from book_manager.repositories import IRepositorio
from book_manager.services.crud_services import ServicioCrud

class GeneroService(ServicioCrud[Genero]):
    """Lógica de los géneros."""

    entidad = "el género"

    def __init__(
        self, repositorio: IRepositorio[Genero], libros: IRepositorio[Libro]
    ) -> None:
        super().__init__(repositorio)
        self._libros = libros

    def _validar(self, entidad: Genero) -> None:
        for genero in self.listar():
            if (
                genero.id != entidad.id
                and genero.nombre.lower() == entidad.nombre.lower()
            ):
                raise ValueError(f"Ya existe el género {entidad.nombre}.")

    def _validar_eliminacion(self, id: int) -> None:
        if any(libro.genero.id == id for libro in self._libros.leer_todos()):
            raise ValueError(
                "No se puede eliminar un género que tiene libros asociados."
            )
