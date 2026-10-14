
import  datetime

from sqlalchemy import select

from decimal import Decimal
from abc import ABC, abstractmethod
from typing import List, Optional
from book_manager.entities import CotizacionDolar
from book_manager.database.connection import ConexionDB
from book_manager.models.models import CotizacionDolarModelo
from book_manager.entities import TipoCotizacion



class IRepositorioCotizacionDolar(ABC):
    """Interfaz para repositorios del tipo RepositorioCotizacionDolar."""

    @abstractmethod
    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        """Crea una nueva cotización de dólar.

        Args:
            cotizacion (CotizacionDolar): El objeto CotizacionDolar a crear.

        Returns:
            CotizacionDolar: El objeto CotizacionDolar creado.

        Raises:
            ValueError: Si ya existe una cotización para el mismo tipo y fecha.
        """
        pass

    @abstractmethod
    def leer_por_tipo_y_fecha(
        self, tipo_id: int, fecha: datetime.date
    ) -> Optional[CotizacionDolar]:
        """Lee una cotización de dólar por tipo y fecha.

        Args:
            tipo_id (int): El ID del tipo de cotización (e.g., 'Oficial',
                'Blue').
            fecha (datetime.date): La fecha de la cotización.

        Returns:
            Optional[CotizacionDolar]: La cotización si se encuentra, None en
                caso contrario.
        """
        pass

    @abstractmethod
    def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
        """Lee el histórico de cotizaciones para un tipo específico.

        Args:
            tipo_id (int): El ID del tipo de cotización.

        Returns:
            List[CotizacionDolar]: Una lista de cotizaciones históricas para
                el tipo dado.
        """
        pass

    @abstractmethod
    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        """Actualiza una cotización de dólar existente.

        Args:
            cotizacion (CotizacionDolar): El objeto CotizacionDolar a
                actualizar.

        Returns:
            CotizacionDolar: El objeto CotizacionDolar actualizado.
        """
        pass

    @abstractmethod
    def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
        """Elimina una cotización de dólar por tipo y fecha.

        Args:
            tipo_id (int): El ID del tipo de cotización.
            fecha (datetime.date): La fecha de la cotización a eliminar.

        Returns:
            bool: True si la cotización fue eliminada, False si no se encontró.
        """
        pass

    @abstractmethod
    def leer_todos(self) -> List[CotizacionDolar]:
        """Devuelve todas las cotizaciones."""
        pass

class RepositorioCotizacionDolar(IRepositorioCotizacionDolar):
    """Repositorio de cotizaciones guardado en CSV.

    La clave es el par (tipo, fecha).
    """

    def __init__(self, conexion: ConexionDB) -> None:
        self._conexion = conexion

    def _a_entidad(
            self,
            modelo: CotizacionDolarModelo
    ) -> CotizacionDolar:
        """Convierte un modelo de SQLAlchemy en una entidad CotizacionDolar."""

        tipo_modelo = modelo.tipo

        tipo = TipoCotizacion(
            tipo_modelo.id,
            tipo_modelo.codigo,
            tipo_modelo.nombre
        )

        return CotizacionDolar(
            tipo,
            modelo.fecha,
            float(modelo.compra),
            float(modelo.venta)
        )

    def crear(
            self,
            cotizacion: CotizacionDolar
    ) -> CotizacionDolar:
        """Crea una nueva cotización de dólar."""
        
        with self._conexion.transaccion() as sesion:

            clave = (
                cotizacion.tipo.id,
                cotizacion.fecha
            )

            if sesion.get(CotizacionDolarModelo, clave) is not None:
                raise ValueError(
                    f"Ya existe una cotización para tipo {cotizacion.tipo.id} "
                )

            modelo = CotizacionDolarModelo(
                tipo_id=cotizacion.tipo.id,
                fecha=cotizacion.fecha,
                compra=Decimal(str(cotizacion.compra)),
                venta=Decimal(str(cotizacion.venta))
            )

            sesion.add(modelo)
            sesion.flush()

            return self._a_entidad(modelo)

    def leer_por_tipo_y_fecha(
            self,
            tipo_id: int,
            fecha: datetime.date
            ) -> Optional[CotizacionDolar]:
        """Lee una cotización de dólar por tipo y fecha."""
        
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(
                CotizacionDolarModelo,
                (tipo_id, fecha)
            )

            return None if modelo is None else self._a_entidad(modelo)

    def leer_historico_por_tipo(
            self,
            tipo_id: int
    ) -> List[CotizacionDolar]:
        """Lee el histórico de cotizaciones para un tipo específico."""
        
        with self._conexion.transaccion() as sesion:
            query = (
                select(CotizacionDolarModelo)
                .where(CotizacionDolarModelo.tipo_id == tipo_id)
                .order_by(CotizacionDolarModelo.fecha)
            )

            modelos = sesion.scalars(query).all()

            return [self._a_entidad(modelo) for modelo in modelos]

    def leer_todos(
            self
    ) -> List[CotizacionDolar]:
        """Devuelve todas las cotizaciones."""
        
        with self._conexion.transaccion() as sesion:
            query = select(CotizacionDolarModelo).order_by(
                CotizacionDolarModelo.tipo_id,
                CotizacionDolarModelo.fecha
            )

            modelos = sesion.scalars(query).all()

            return [self._a_entidad(modelo) for modelo in modelos]

    def actualizar(
            self,
            cotizacion: CotizacionDolar
    ) -> CotizacionDolar:
        """Actualiza una cotización de dólar existente."""
        
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(
                CotizacionDolarModelo,
                (
                    cotizacion.tipo.id,
                    cotizacion.fecha
                  )
            )

            if modelo is None:
                raise ValueError(
                    f"No se encontró la cotización para tipo {cotizacion.tipo.id} "
                )

            modelo.compra = Decimal(str(cotizacion.compra))
            modelo.venta = Decimal(str(cotizacion.venta))
            sesion.flush()

            return self._a_entidad(modelo)

    def eliminar(
            self,
            tipo_id: int,
            fecha: datetime.date
    ) -> bool:
        """Elimina una cotización de dólar por tipo y fecha."""
        
        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(
                CotizacionDolarModelo,
                (tipo_id, fecha)
            )

            if modelo is None:
                return False

            sesion.delete(modelo)
            sesion.flush()

            return True

        