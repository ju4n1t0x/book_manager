import datetime
from book_manager.entities.entidad_base_model import _validar_positivo
from book_manager.entities.tipo_cotizacion_model import TipoCotizacion


class CotizacionDolar:
    """Cotización del dólar para un tipo y una fecha.

    Se identifica por el par (tipo, fecha).
    """

    def __init__(
        self,
        tipo: TipoCotizacion,
        fecha: datetime.date,
        compra: float,
        venta: float,
    ) -> None:
        self.tipo = tipo
        self.fecha = fecha
        self.compra = compra
        self.venta = venta

    @property
    def tipo(self) -> TipoCotizacion:
        return self._tipo

    @tipo.setter
    def tipo(self, valor: TipoCotizacion) -> None:
        if not isinstance(valor, TipoCotizacion):
            raise ValueError("La cotización debe tener un tipo válido.")
        self._tipo = valor

    @property
    def tipo_id(self) -> int:
        return self._tipo.id

    @property
    def fecha(self) -> datetime.date:
        return self._fecha

    @fecha.setter
    def fecha(self, valor: datetime.date) -> None:
        if not isinstance(valor, datetime.date):
            raise ValueError("La fecha de la cotización no es válida.")
        if valor > datetime.date.today():
            raise ValueError("La fecha de la cotización no puede ser futura.")
        self._fecha = valor

    @property
    def compra(self) -> float:
        return self._compra

    @compra.setter
    def compra(self, valor: float) -> None:
        self._compra = _validar_positivo(valor, "compra")

    @property
    def venta(self) -> float:
        return self._venta

    @venta.setter
    def venta(self, valor: float) -> None:
        self._venta = _validar_positivo(valor, "venta")

    def __str__(self) -> str:
        return (
            f"{self.tipo.nombre} {self.fecha}: "
            f"compra $ {self.compra:,.2f} / venta $ {self.venta:,.2f}"
        )