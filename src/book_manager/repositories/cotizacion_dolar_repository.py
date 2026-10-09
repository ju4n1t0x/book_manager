
import abc, datetime

from pathlib import Path
from typing import List, Optional
from book_manager.entities import CotizacionDolar
from book_manager.repositories.tipo_cotizacion_repository import RepositorioTipoCotizacion
from book_manager.repositories.archivo_csv_repository import ArchivoCSV



class IRepositorioCotizacionDolar(abc.ABC):
    """Interfaz para repositorios del tipo RepositorioCotizacionDolar."""

    @abc.abstractmethod
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

    @abc.abstractmethod
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

    @abc.abstractmethod
    def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
        """Lee el histórico de cotizaciones para un tipo específico.

        Args:
            tipo_id (int): El ID del tipo de cotización.

        Returns:
            List[CotizacionDolar]: Una lista de cotizaciones históricas para
                el tipo dado.
        """
        pass

    @abc.abstractmethod
    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        """Actualiza una cotización de dólar existente.

        Args:
            cotizacion (CotizacionDolar): El objeto CotizacionDolar a
                actualizar.

        Returns:
            CotizacionDolar: El objeto CotizacionDolar actualizado.
        """
        pass

    @abc.abstractmethod
    def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
        """Elimina una cotización de dólar por tipo y fecha.

        Args:
            tipo_id (int): El ID del tipo de cotización.
            fecha (datetime.date): La fecha de la cotización a eliminar.

        Returns:
            bool: True si la cotización fue eliminada, False si no se encontró.
        """
        pass

    @abc.abstractmethod
    def leer_todos(self) -> List[CotizacionDolar]:
        """Devuelve todas las cotizaciones."""
        pass

class RepositorioCotizacionDolar(IRepositorioCotizacionDolar):
    """Repositorio de cotizaciones guardado en CSV.

    La clave es el par (tipo, fecha).
    """

    campos = ["tipo_id", "fecha", "compra", "venta"]

    def __init__(self, ruta: Path, tipos: RepositorioTipoCotizacion) -> None:
        self._tipos = tipos
        self._archivo = ArchivoCSV(ruta, self.campos)
        self._cotizaciones: dict[
            tuple[int, datetime.date], CotizacionDolar
        ] = {}
        for fila in self._archivo.leer():
            cotizacion = self._desde_fila(fila)
            self._cotizaciones[(cotizacion.tipo_id, cotizacion.fecha)] = (
                cotizacion
            )

    def _a_fila(self, cotizacion: CotizacionDolar) -> dict:
        return {
            "tipo_id": cotizacion.tipo_id,
            "fecha": cotizacion.fecha.isoformat(),
            "compra": cotizacion.compra,
            "venta": cotizacion.venta,
        }

    def _desde_fila(self, fila: dict[str, str]) -> CotizacionDolar:
        tipo = self._tipos.leer_por_id(int(fila["tipo_id"]))
        if tipo is None:
            raise ValueError(
                "Hay cotizaciones de un tipo que no existe "
                f"({fila['tipo_id']})."
            )
        fecha = datetime.date.fromisoformat(fila["fecha"])
        return CotizacionDolar(
            tipo, fecha, float(fila["compra"]), float(fila["venta"])
        )

    def _guardar(self) -> None:
        ordenadas = sorted(
            self._cotizaciones.values(), key=lambda c: (c.tipo_id, c.fecha)
        )
        self._archivo.escribir([self._a_fila(c) for c in ordenadas])

    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        clave = (cotizacion.tipo_id, cotizacion.fecha)
        if clave in self._cotizaciones:
            raise ValueError(
                f"Ya existe una cotización {cotizacion.tipo.nombre} "
                f"del {cotizacion.fecha}."
            )
        self._cotizaciones[clave] = cotizacion
        self._guardar()
        return cotizacion

    def leer_por_tipo_y_fecha(
        self, tipo_id: int, fecha: datetime.date
    ) -> Optional[CotizacionDolar]:
        return self._cotizaciones.get((tipo_id, fecha))

    def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
        historico = [
            c for c in self._cotizaciones.values() if c.tipo_id == tipo_id
        ]
        return sorted(historico, key=lambda c: c.fecha)

    def leer_todos(self) -> List[CotizacionDolar]:
        """Devuelve todas las cotizaciones ordenadas por tipo y fecha."""
        return sorted(
            self._cotizaciones.values(), key=lambda c: (c.tipo_id, c.fecha)
        )

    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        clave = (cotizacion.tipo_id, cotizacion.fecha)
        if clave not in self._cotizaciones:
            raise ValueError(
                f"No existe una cotización {cotizacion.tipo.nombre} "
                f"del {cotizacion.fecha}."
            )
        self._cotizaciones[clave] = cotizacion
        self._guardar()
        return cotizacion

    def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
        if (tipo_id, fecha) not in self._cotizaciones:
            return False
        del self._cotizaciones[(tipo_id, fecha)]
        self._guardar()
        return True
