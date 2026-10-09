
from book_manager.entities import Editorial, Libro
from book_manager.repositories import IRepositorio
from book_manager.services.crud_services import ServicioCrud

class EditorialService(ServicioCrud[Editorial]):
    """Lógica de las editoriales."""

    entidad = "la editorial"

    def __init__(
        self, repositorio: IRepositorio[Editorial], libros: IRepositorio[Libro]
    ) -> None:
        super().__init__(repositorio)
        self._libros = libros

    def _validar(self, entidad: Editorial) -> None:
        for editorial in self.listar():
            if (
                editorial.id != entidad.id
                and editorial.nombre.lower() == entidad.nombre.lower()
            ):
                raise ValueError(f"Ya existe la editorial {entidad.nombre}.")

    def _validar_eliminacion(self, id: int) -> None:
        if any(
            libro.editorial.id == id for libro in self._libros.leer_todos()
        ):
            raise ValueError(
                "No se puede eliminar una editorial que tiene libros "
                "asociados."
            )
