

from typing import List
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session
from book_manager.entities import Precio
from book_manager.repositories.sqlalchemy_repository import RepositorioSqlAlchemy

from book_manager.entities import (
    Editorial,
    Genero,
    Libro,
    Moneda,
    Precio
)

from book_manager.models.models import (
    LibroModelo,
    MonedaModelo,
    PrecioModelo
)


class RepositorioPrecio(RepositorioSqlAlchemy[Precio, PrecioModelo]):
    """Repositorio de precios."""

    modelo = PrecioModelo

    def _convertir_libro(
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

    def _convertir_moneda(
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

    def _a_entidad(
            self,
            modelo: PrecioModelo
    ) -> Precio:
        """Convierte un modelo de SQLAlchemy a una entidad de dominio."""

        libro = self._convertir_libro(modelo.libro)
        moneda = self._convertir_moneda(modelo.moneda)

        return Precio(
            modelo.id,
            libro,
            moneda,
            float(modelo.monto)
        )

    def _obtener_libro(
            self,
            sesion: Session,
            libro_id: int
    ) -> LibroModelo:
        """Obtiene un modelo de libro por su ID."""

        libro = sesion.get(LibroModelo, libro_id)

        if libro is None:
            raise ValueError(f"No se encontró el libro con id {libro_id}")

        return libro

    def _obtener_moneda(
            self,
            sesion: Session,
            moneda_id: int
    ) -> MonedaModelo:
        """Obtiene un modelo de moneda por su ID."""

        moneda = sesion.get(MonedaModelo, moneda_id)

        if moneda is None:
            raise ValueError(f"No se encontró la moneda con id {moneda_id}")

        return moneda

    def _crear_modelo(
            self,
            sesion: Session,
            entidad: Precio
    ) -> PrecioModelo:
        """Crea un modelo de SQLAlchemy a partir de una entidad de dominio."""

        libro = self._obtener_libro(
            sesion,
            entidad.libro.id
            )
        moneda = self._obtener_moneda(
            sesion, 
            entidad.moneda.id
            )

        return PrecioModelo(
            libro=libro,
            moneda=moneda,
            monto=entidad.monto
        )

    def _actualizar_modelo(
            self,
            sesion: Session,
            modelo: PrecioModelo,
            entidad: Precio
    ) -> None:
        """Actualiza un modelo de SQLAlchemy a partir de una entidad de dominio."""

        libro = self._obtener_libro(
             sesion,
             entidad.libro.id
        )

        moneda = self._obtener_moneda(
            sesion,
            entidad.moneda.id
        )
    
        modelo.libro_id = libro.id
        modelo.moneda_id = moneda.id
        modelo.monto = Decimal(str(entidad.monto))

    def leer_por_libro(
            self,
            libro_id: int,
    ) -> List[Precio]:
        """Lee todos los precios asociados a un libro por su ID."""

        with self._conexion.transaccion() as sesion:
            query = (
                select(PrecioModelo)
                .where(PrecioModelo.libro_id == libro_id)
                .order_by(PrecioModelo.id)
            )

            modelos = sesion.scalars(query).all()

            return[
                self._a_entidad(modelo)
                for modelo in modelos
            ]