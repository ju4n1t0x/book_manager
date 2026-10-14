from sqlalchemy.orm import Session

from book_manager.entities import Genero
from book_manager.models.models import GeneroModelo
from book_manager.repositories.sqlalchemy_repository import RepositorioSqlAlchemy
from book_manager.database.connection import ConexionDB




class RepositorioGenero(RepositorioSqlAlchemy[Genero, GeneroModelo]):
    """Repositorio de géneros."""

    modelo = GeneroModelo

    def __init__(self, conexion: ConexionDB) -> None:
        super().__init__(conexion)

    def _a_entidad(
            self, 
            modelo: GeneroModelo
            ) -> Genero:
        """Convierte un modelo de SQLAlchemy a una entidad de dominio."""
        return Genero(
            modelo.id,
            modelo.nombre,
            modelo.descripcion
        )

    def _crear_modelo(
            self,
            sesion: Session,
            entidad: Genero
            ) -> GeneroModelo:
        """Crea un modelo de SQLAlchemy a partir de una entidad de dominio."""
        return GeneroModelo(
            nombre=entidad.nombre,
            descripcion=entidad.descripcion
        )

    def _actualizar_modelo(
            self,
            sesion: Session,
            modelo: GeneroModelo,
            entidad: Genero
            ) -> None:
        """Actualiza un modelo de SQLAlchemy a partir de una entidad de dominio."""
        modelo.nombre = entidad.nombre
        modelo.descripcion = entidad.descripcion

