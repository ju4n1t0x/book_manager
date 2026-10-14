from sqlalchemy.orm import Session

from book_manager.database.connection import ConexionDB
from book_manager.entities import TipoCotizacion
from book_manager.models.models import TipoCotizacionModelo
from book_manager.repositories.sqlalchemy_repository import (
    RepositorioSqlAlchemy,
)


class RepositorioTipoCotizacion(
    RepositorioSqlAlchemy[TipoCotizacion, TipoCotizacionModelo]
):
    """Repositorio de tipos de cotización en PostgreSQL."""

    campos = ["id", "codigo", "nombre"]
    modelo = TipoCotizacionModelo

    def __init__(self, conexion: ConexionDB) -> None:
        """Inicializa el repositorio con la conexión a la base."""
        super().__init__(conexion)

    def _a_entidad(
        self, modelo: TipoCotizacionModelo
    ) -> TipoCotizacion:
        """Convierte un modelo SQLAlchemy en una entidad."""

        return TipoCotizacion(
            modelo.id,
            modelo.codigo,
            modelo.nombre,
        )

    def _crear_modelo(
        self,
        sesion: Session,
        entidad: TipoCotizacion,
    ) -> TipoCotizacionModelo:
        """Crea un modelo SQLAlchemy desde una entidad."""

        return TipoCotizacionModelo(
            codigo=entidad.codigo,
            nombre=entidad.nombre,
        )

    def _actualizar_modelo(
        self,
        sesion: Session,
        modelo: TipoCotizacionModelo,
        entidad: TipoCotizacion,
    ) -> None:
        """Actualiza un modelo SQLAlchemy existente."""

        modelo.codigo = entidad.codigo
        modelo.nombre = entidad.nombre