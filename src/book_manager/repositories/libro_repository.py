
from pathlib import Path
from book_manager.repositories.archivo_csv_repository import RepositorioCSV
from book_manager.repositories.editorial_repository import RepositorioEditorial
from book_manager.repositories.genero_repository import RepositorioGenero

from book_manager.entities import (
    Libro,  
)



class RepositorioLibro(RepositorioCSV[Libro]):
    """Repositorio de libros.

    En el archivo se guardan los ids de la editorial y el género; al leer
    se buscan en sus repositorios para armar el libro completo.
    """

    campos = [
        "id",
        "isbn",
        "titulo",
        "autor",
        "editorial_id",
        "genero_id",
        "anio_publicacion",
    ]

    def __init__(
        self,
        ruta: Path,
        editoriales: RepositorioEditorial,
        generos: RepositorioGenero,
    ) -> None:
        self._editoriales = editoriales
        self._generos = generos
        super().__init__(ruta)

    def _a_fila(self, entidad: Libro) -> dict:
        return {
            "id": entidad.id,
            "isbn": entidad.isbn,
            "titulo": entidad.titulo,
            "autor": entidad.autor,
            "editorial_id": entidad.editorial.id,
            "genero_id": entidad.genero.id,
            "anio_publicacion": entidad.anio_publicacion,
        }

    def _desde_fila(self, fila: dict[str, str]) -> Libro:
        editorial = self._editoriales.leer_por_id(int(fila["editorial_id"]))
        genero = self._generos.leer_por_id(int(fila["genero_id"]))
        if editorial is None or genero is None:
            raise ValueError(
                f"El libro {fila['id']} tiene una editorial o un género "
                "que no existe."
            )
        return Libro(
            int(fila["id"]),
            fila["isbn"],
            fila["titulo"],
            fila["autor"],
            editorial,
            genero,
            int(fila["anio_publicacion"]),
        )