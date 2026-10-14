
from sqlalchemy.orm import Session

from book_manager.entities import Moneda
from book_manager.models.models import MonedaModelo
from book_manager.repositories.sqlalchemy_repository import RepositorioSqlAlchemy
from book_manager.database.connection import ConexionDB
from book_manager.repositories.irepositorio import IRepositorio
from abc import ABC


class IRepositorioMoneda(IRepositorio[Moneda], ABC):
    """Interfaz del repositorio de monedas."""
    pass

class RepositorioMoneda(RepositorioSqlAlchemy[Moneda, MonedaModelo]):
    """Repositorio de monedas."""

    modelo = MonedaModelo

    """Repositorio de monedas."""

    def __init__(self, conexion: ConexionDB) -> None:
            super().__init__(conexion)

    def _a_entidad(
            self,
            modelo: MonedaModelo
    ) -> Moneda:
        """Convierte un modelo de SQLAlchemy a una entidad de dominio."""

        return Moneda(
            modelo.id,
            modelo.codigo,
            modelo.nombre,
            modelo.simbolo
        )

    def _crear_modelo(
            self,
            sesion: Session,
            entidad: Moneda
    ) -> MonedaModelo:
        """Crea un modelo de SQLAlchemy a partir de una entidad de dominio."""

        return MonedaModelo(
            codigo=entidad.codigo,
            nombre=entidad.nombre,
            simbolo=entidad.simbolo
        )

    def _actualizar_modelo(
            self, 
            sesion: Session,
            modelo: MonedaModelo,
            entidad: Moneda,
    ) -> None:
        """Actualiza un modelo de SQLAlchemy a partir de una entidad de dominio."""

        modelo.codigo = entidad.codigo
        modelo.nombre = entidad.nombre
        modelo.simbolo = entidad.simbolo
