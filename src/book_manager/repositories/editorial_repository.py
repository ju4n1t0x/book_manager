from sqlalchemy.orm import Session

from book_manager.entities import Editorial
from book_manager.models.models import EditorialModelo
from book_manager.repositories.sqlalchemy_repository import RepositorioSqlAlchemy
from book_manager.database.connection import ConexionDB
from book_manager.repositories.irepositorio import IRepositorio
from abc import ABC


class IRepositorioEditorial(IRepositorio[Editorial], ABC):
    """Interfaz del repositorio de editoriales."""
    pass

class RepositorioEditorial(RepositorioSqlAlchemy[Editorial, EditorialModelo]):
    """Repositorio de editoriales."""

    modelo = EditorialModelo

    """Repositorio de editoriales."""

    def __init__(self, conexion: ConexionDB) -> None:
        super().__init__(conexion)

    def _a_entidad(
            self,
            modelo: EditorialModelo
            ) -> Editorial:
        """Convierte un modelo de SQLAlchemy a una entidad de dominio."""
        return Editorial(
            modelo.id,
            modelo.nombre,
            modelo.pais,
            modelo.sitio_web
        )

    def _crear_modelo(
            self,
            sesion: Session,
            entidad: Editorial
            ) -> EditorialModelo:
        """Crea un modelo de SQLAlchemy a partir de una entidad de dominio."""
        return EditorialModelo(
            nombre=entidad.nombre,
            pais=entidad.pais,
            sitio_web=entidad.sitio_web
        ) 

    def _actualizar_modelo(
            self,
            sesion: Session,
            modelo: EditorialModelo,
            entidad: Editorial
            ) -> None:
        """Actualiza un modelo de SQLAlchemy a partir de una entidad de dominio."""
        modelo.nombre = entidad.nombre
        modelo.pais = entidad.pais
        modelo.sitio_web = entidad.sitio_web
    
