
import abc, json, urllib.error, urllib.request, datetime

from typing import List, NamedTuple, Optional
from book_manager.services.precio_service import PrecioService
from book_manager.services.tipo_cotizacion_service import TipoCotizacionService


from book_manager.entities import (
    CotizacionDolar,
    Precio,

)
from book_manager.repositories import (
    IRepositorioCotizacionDolar,
)  


class CotizacionExterna(NamedTuple):
    """Cotización tal como la devuelve un proveedor externo."""

    codigo: str
    compra: float
    venta: float


class ProveedorCotizaciones(abc.ABC):
    """Fuente de donde se obtienen las cotizaciones del día."""

    @abc.abstractmethod
    def obtener(self) -> List[CotizacionExterna]:
        """Devuelve las cotizaciones actuales.

        Raises:
            ConnectionError: Si no se pudo consultar la fuente.
        """


class DolarApi(ProveedorCotizaciones):
    """Consulta las cotizaciones del dólar en https://dolarapi.com."""

    URL = "https://dolarapi.com/v1/dolares"

    def __init__(self, timeout: int = 5) -> None:
        self._timeout = timeout

    def obtener(self) -> List[CotizacionExterna]:
        """Consulta la API y devuelve una cotización por cada tipo de dólar.

        La API responde 403 si el pedido no tiene User-Agent, por eso se arma
        el Request con ese encabezado.
        """
        pedido = urllib.request.Request(
            self.URL, headers={"User-Agent": "book-manager"}
        )
        try:
            with urllib.request.urlopen(
                pedido, timeout=self._timeout
            ) as respuesta:
                datos = json.load(respuesta)
        except (
            urllib.error.URLError,
            TimeoutError,
            json.JSONDecodeError,
        ) as error:
            raise ConnectionError(
                f"No se pudo consultar DolarApi: {error}"
            ) from error

        return [
            CotizacionExterna(
                dato["casa"], float(dato["compra"]), float(dato["venta"])
            )
            for dato in datos
            if dato.get("compra") and dato.get("venta")
        ]


class CotizacionService:
    """Lógica de las cotizaciones del dólar."""

    def __init__(
        self,
        repositorio: IRepositorioCotizacionDolar,
        tipos: TipoCotizacionService,
        proveedor: ProveedorCotizaciones,
    ) -> None:
        self._repositorio = repositorio
        self._tipos = tipos
        self._proveedor = proveedor

    def listar(self) -> List[CotizacionDolar]:
        return self._repositorio.leer_todos()

    def historico(self, tipo_id: int) -> List[CotizacionDolar]:
        self._tipos.buscar(tipo_id)
        return self._repositorio.leer_historico_por_tipo(tipo_id)

    def ultima(self, tipo_id: int) -> Optional[CotizacionDolar]:
        """Devuelve la cotización más reciente de un tipo.

        Returns:
            Optional[CotizacionDolar]: La cotización, o None si no hay
                ninguna.
        """
        historico = self._repositorio.leer_historico_por_tipo(tipo_id)
        return historico[-1] if historico else None

    def buscar(self, tipo_id: int, fecha: datetime.date) -> CotizacionDolar:
        cotizacion = self._repositorio.leer_por_tipo_y_fecha(tipo_id, fecha)
        if cotizacion is None:
            raise ValueError(
                f"No hay cotización del tipo {tipo_id} para el {fecha}."
            )
        return cotizacion

    def crear(
        self, tipo_id: int, fecha: datetime.date, compra: float, venta: float
    ) -> CotizacionDolar:
        tipo = self._tipos.buscar(tipo_id)
        return self._repositorio.crear(
            CotizacionDolar(tipo, fecha, compra, venta)
        )

    def actualizar(
        self, tipo_id: int, fecha: datetime.date, compra: float, venta: float
    ) -> CotizacionDolar:
        cotizacion = self.buscar(tipo_id, fecha)
        nueva = CotizacionDolar(cotizacion.tipo, fecha, compra, venta)
        return self._repositorio.actualizar(nueva)

    def eliminar(self, tipo_id: int, fecha: datetime.date) -> None:
        if not self._repositorio.eliminar(tipo_id, fecha):
            raise ValueError(
                f"No hay cotización del tipo {tipo_id} para el {fecha}."
            )

    def actualizar_desde_api(self) -> int:
        """Trae las cotizaciones del día y las guarda.

        Si ya había una cotización de hoy para ese tipo, se pisa con la nueva.
        Los tipos que no están dados de alta en el sistema se ignoran.

        Returns:
            int: Cantidad de cotizaciones guardadas.

        Raises:
            ConnectionError: Si no se pudo consultar la API.
        """
        hoy = datetime.date.today()
        guardadas = 0
        for externa in self._proveedor.obtener():
            tipo = self._tipos.buscar_por_codigo(externa.codigo)
            if tipo is None:
                continue
            cotizacion = CotizacionDolar(
                tipo, hoy, externa.compra, externa.venta
            )
            if self._repositorio.leer_por_tipo_y_fecha(tipo.id, hoy):
                self._repositorio.actualizar(cotizacion)
            else:
                self._repositorio.crear(cotizacion)
            guardadas += 1
        return guardadas

class CotizadorService:
    """Calcula el precio de los libros en pesos según cada tipo de dólar."""

    def __init__(
        self,
        precios: PrecioService,
        cotizaciones: CotizacionService,
        tipos: TipoCotizacionService,
    ) -> None:
        self._precios = precios
        self._cotizaciones = cotizaciones
        self._tipos = tipos

    @staticmethod
    def a_pesos(
        precio: Precio, cotizacion: CotizacionDolar
    ) -> Optional[float]:
        """Convierte un precio a pesos con el valor de venta de la cotización.

        Returns:
            Optional[float]: El monto en pesos, o None si la moneda no es ARS
                ni USD.
        """
        match precio.moneda.codigo:
            case "ARS":
                return precio.monto
            case "USD":
                return round(precio.monto * cotizacion.venta, 2)
            case _:
                return None

    def _precio_base(self, libro_id: int) -> Optional[Precio]:
        """Devuelve el precio que se usa para cotizar el libro.

        Si tiene precio en dólares se usa ese, porque es el que depende de la
        cotización; si no, el precio en pesos.
        """
        precios = self._precios.precios_de_libro(libro_id)
        en_dolares = [p for p in precios if p.moneda.codigo == "USD"]
        en_pesos = [p for p in precios if p.moneda.codigo == "ARS"]
        return (en_dolares or en_pesos or [None])[0]

    def cotizar_libro(
        self, libro_id: int
    ) -> List[tuple[CotizacionDolar, float, float]]:
        """Precio del libro en pesos y en dólares con cada tipo de cotización.

        Solo se incluyen los tipos que tienen al menos una cotización cargada.

        Returns:
            List[tuple[CotizacionDolar, float, float]]: Cotización usada,
                precio en pesos y precio en dólares.

        Raises:
            ValueError: Si el libro no tiene precio en ARS ni en USD.
        """
        precio = self._precio_base(libro_id)
        if precio is None:
            raise ValueError("El libro no tiene precio en ARS ni en USD.")
        resultado = []
        for tipo in self._tipos.listar():
            cotizacion = self._cotizaciones.ultima(tipo.id)
            if cotizacion is not None:
                pesos = self.a_pesos(precio, cotizacion)
                resultado.append(
                    (cotizacion, pesos, round(pesos / cotizacion.venta, 2))
                )
        return resultado

    def precio_en_pesos(self, libro_id: int, tipo_id: int) -> Optional[float]:
        """Precio del libro en pesos con la última cotización de un tipo.

        Returns:
            Optional[float]: El precio, o None si falta el precio o la
                cotización.
        """
        precio = self._precio_base(libro_id)
        cotizacion = self._cotizaciones.ultima(tipo_id)
        if precio is None or cotizacion is None:
            return None
        return self.a_pesos(precio, cotizacion)


