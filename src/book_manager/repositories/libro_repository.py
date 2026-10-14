from typing import Optional
from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.orm import Session
from book_manager.repositories.sqlalchemy_repository import RepositorioSqlAlchemy
from book_manager.repositories.irepositorio import IRepositorio


from book_manager.entities import (
    Libro,
    Genero,
    Editorial,
)

from book_manager.models.models import (
    LibroModelo,
    GeneroModelo,
    EditorialModelo
)

class IRepositorioLibro(IRepositorio[Libro], ABC):
    @abstractmethod
    def leer_por_isbn(
            self,
            isbn: str
    ) -> Optional[Libro]:
        """Lee un libro por su ISBN."""
        pass

class RepositorioLibro(RepositorioSqlAlchemy[Libro, LibroModelo], IRepositorioLibro):
    """Repositorio de libros.

    En el archivo se guardan los ids de la editorial y el género; al leer
    se buscan en sus repositorios para armar el libro completo.
    """

    modelo = LibroModelo

 
    def _a_entidad(
            self,
            modelo: LibroModelo
    ) -> Libro:
        """Convierte un modelo de SQLAlchemy a una entidad de dominio."""

        editorial = Editorial(
            modelo.editorial.id,
            modelo.editorial.nombre,
            modelo.editorial.pais,
            modelo.editorial.sitio_web
        )

        genero = Genero(
            modelo.genero.id,
            modelo.genero.nombre,
            modelo.genero.descripcion
        )

        return Libro(
            modelo.id,
            modelo.isbn,
            modelo.titulo,
            modelo.autor,
            editorial,
            genero,
            modelo.anio_publicacion
        )

    def _obtener_editorial(
           self,
           sesion: Session,
           editorial_id: int
    ) -> EditorialModelo:
        """Obtiene un modelo de editorial por su ID."""

        editorial = sesion.get(EditorialModelo, editorial_id)

        if editorial is None:
            raise ValueError(f"No se encontró la editorial con id {editorial_id}")

        return editorial

    def _obtener_genero(
            self,
            sesion: Session,
            genero_id: int
    ) -> GeneroModelo:
        """Obtiene un modelo de género por su ID."""

        genero = sesion.get(GeneroModelo, genero_id)

        if genero is None:
            raise ValueError(f"No se encontró el género con id {genero_id}")

        return genero

    def _crear_modelo(
            self,
            sesion: Session,
            entidad: Libro
    ) -> LibroModelo:
        """Crea un modelo de SQLAlchemy a partir de una entidad de dominio."""

        editorial = self._obtener_editorial(
            sesion,
            entidad.editorial.id,
            )

        genero = self._obtener_genero(
            sesion,
            entidad.genero.id,
        )

        return LibroModelo(
            isbn=entidad.isbn,
            titulo=entidad.titulo,
            autor=entidad.autor,
            editorial=editorial,
            genero=genero,
            anio_publicacion=entidad.anio_publicacion
            )

    def _actualizar_modelo(
            self,
            sesion: Session,
            modelo: LibroModelo,
            entidad: Libro
    ) -> None:
        """Actualiza un modelo de SQLAlchemy a partir 
        de una entidad de dominio."""

        modelo.isbn = entidad.isbn
        modelo.titulo = entidad.titulo
        modelo.autor = entidad.autor
        modelo.anio_publicacion = entidad.anio_publicacion

        if modelo.editorial.id != entidad.editorial.id:
            editorial = self._obtener_editorial(
                sesion, 
                entidad.editorial.id
            )
            modelo.editorial = editorial

        if modelo.genero.id != entidad.genero.id:
            genero = self._obtener_genero(
                sesion,
                entidad.genero.id
            )
            modelo.genero = genero

    def leer_por_isbn(
            self,
            isbn: str
            ) -> Optional[Libro]:
        """Lee un libro por su ISBN."""

        with self._conexion.transaccion() as sesion:
            query = select(LibroModelo).where(
                LibroModelo.isbn == isbn
            )

            modelo = sesion.scalars(query).first()

            if modelo is None:
                return None

            return self._a_entidad(modelo)
