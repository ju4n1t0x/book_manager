
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from book_manager.models.models import TipoCotizacionModelo
from book_manager.entities import TipoCotizacion
from book_manager.repositories.sqlalchemy_repository import RepositorioSqlAlchemy
from book_manager.database.connection import ConexionDB
from book_manager.repositories.irepositorio import IRepositorio

class IRepositorioTipoCotizacion(IRepositorio[TipoCotizacion], ABC):
    """Interfaz del repositorio de tipos de cotización."""
    pass


class RepositorioTipoCotizacion(RepositorioSqlAlchemy[TipoCotizacion, TipoCotizacionModelo]):
    """Repositorio de tipos de cotización."""

    modelo = TipoCotizacionModelo

    def __init__(self, conexion: ConexionDB) -> None:
            super().__init__(conexion)

    def _a_entidad(
            self,
            modelo: TipoCotizacionModelo
    ) -> TipoCotizacion:
        """Convierte un modelo de SQLAlchemy a una entidad de dominio."""

        return TipoCotizacion(
            modelo.id,
            modelo.codigo,
            modelo.nombre
    )

    def _crear_modelo(
            self,
            sesion: Session,
            entidad: TipoCotizacion
    ) -> TipoCotizacionModelo:
        """Crea un modelo de SQLAlchemy a partir de una entidad de dominio."""

        return TipoCotizacionModelo(
            codigo=entidad.codigo,
            nombre=entidad.nombre
        )

    def _actualizar_modelo(
            self,
            sesion: Session,
            modelo: TipoCotizacionModelo,
            entidad: TipoCotizacion
    ) -> None:
        """Actualiza un modelo de SQLAlchemy a partir de una entidad de dominio."""

        modelo.codigo = entidad.codigo
        modelo.nombre = entidad.nombre