"""Lógica de negocio del sistema."""

import abc
import datetime
import json
import urllib.error
import urllib.request
from typing import Generic, List, NamedTuple, Optional, TypeVar

from book_manager.entities.entities import (
    CotizacionDolar,
    Editorial,
    EntidadBase,
    Genero,
    Libro,
    Moneda,
    Precio,
    Stock,
    TipoCotizacion,
)
from book_manager.repositories.repositories import (
    IRepositorio,
    IRepositorioCotizacionDolar,
    IRepositorioStock,
    RepositorioPrecio,
    Repositorios,
)

T = TypeVar("T", bound=EntidadBase)


class ServicioCrud(Generic[T]):
    """Operaciones CRUD comunes a todas las entidades con id.

    Las subclases agregan sus validaciones redefiniendo _validar y
    _validar_eliminacion.
    """

    entidad = "el registro"

    def __init__(self, repositorio: IRepositorio[T]) -> None:
        self._repositorio = repositorio

    def listar(self) -> List[T]:
        return self._repositorio.leer_todos()

    def buscar(self, id: int) -> T:
        """Busca una entidad por id.

        Raises:
            ValueError: Si no existe.
        """
        entidad = self._repositorio.leer_por_id(id)
        if entidad is None:
            raise ValueError(f"No se encontró {self.entidad} con id {id}.")
        return entidad

    def crear(self, entidad: T) -> T:
        self._validar(entidad)
        return self._repositorio.crear(entidad)

    def actualizar(self, entidad: T) -> T:
        self.buscar(entidad.id)
        self._validar(entidad)
        return self._repositorio.actualizar(entidad)

    def eliminar(self, id: int) -> None:
        self.buscar(id)
        self._validar_eliminacion(id)
        self._repositorio.eliminar(id)

    def _validar(self, entidad: T) -> None:
        """Validaciones de negocio antes de crear o actualizar."""

    def _validar_eliminacion(self, id: int) -> None:
        """Validaciones de negocio antes de eliminar."""


class GeneroService(ServicioCrud[Genero]):
    """Lógica de los géneros."""

    entidad = "el género"

    def __init__(
        self, repositorio: IRepositorio[Genero], libros: IRepositorio[Libro]
    ) -> None:
        super().__init__(repositorio)
        self._libros = libros

    def _validar(self, entidad: Genero) -> None:
        for genero in self.listar():
            if (
                genero.id != entidad.id
                and genero.nombre.lower() == entidad.nombre.lower()
            ):
                raise ValueError(f"Ya existe el género {entidad.nombre}.")

    def _validar_eliminacion(self, id: int) -> None:
        if any(libro.genero.id == id for libro in self._libros.leer_todos()):
            raise ValueError(
                "No se puede eliminar un género que tiene libros asociados."
            )


class EditorialService(ServicioCrud[Editorial]):
    """Lógica de las editoriales."""

    entidad = "la editorial"

    def __init__(
        self, repositorio: IRepositorio[Editorial], libros: IRepositorio[Libro]
    ) -> None:
        super().__init__(repositorio)
        self._libros = libros

    def _validar(self, entidad: Editorial) -> None:
        for editorial in self.listar():
            if (
                editorial.id != entidad.id
                and editorial.nombre.lower() == entidad.nombre.lower()
            ):
                raise ValueError(f"Ya existe la editorial {entidad.nombre}.")

    def _validar_eliminacion(self, id: int) -> None:
        if any(
            libro.editorial.id == id for libro in self._libros.leer_todos()
        ):
            raise ValueError(
                "No se puede eliminar una editorial que tiene libros "
                "asociados."
            )


class MonedaService(ServicioCrud[Moneda]):
    """Lógica de las monedas."""

    entidad = "la moneda"

    def __init__(
        self, repositorio: IRepositorio[Moneda], precios: IRepositorio[Precio]
    ) -> None:
        super().__init__(repositorio)
        self._precios = precios

    def buscar_por_codigo(self, codigo: str) -> Optional[Moneda]:
        return next(
            (m for m in self.listar() if m.codigo == codigo.upper()), None
        )

    def _validar(self, entidad: Moneda) -> None:
        existente = self.buscar_por_codigo(entidad.codigo)
        if existente is not None and existente.id != entidad.id:
            raise ValueError(f"Ya existe la moneda {entidad.codigo}.")

    def _validar_eliminacion(self, id: int) -> None:
        if any(
            precio.moneda.id == id for precio in self._precios.leer_todos()
        ):
            raise ValueError(
                "No se puede eliminar una moneda que se usa en algún precio."
            )


class TipoCotizacionService(ServicioCrud[TipoCotizacion]):
    """Lógica de los tipos de cotización."""

    entidad = "el tipo de cotización"

    def __init__(
        self,
        repositorio: IRepositorio[TipoCotizacion],
        cotizaciones: IRepositorioCotizacionDolar,
    ) -> None:
        super().__init__(repositorio)
        self._cotizaciones = cotizaciones

    def buscar_por_codigo(self, codigo: str) -> Optional[TipoCotizacion]:
        return next(
            (t for t in self.listar() if t.codigo == codigo.lower()), None
        )

    def _validar(self, entidad: TipoCotizacion) -> None:
        existente = self.buscar_por_codigo(entidad.codigo)
        if existente is not None and existente.id != entidad.id:
            raise ValueError(
                f"Ya existe el tipo de cotización con código {entidad.codigo}."
            )

    def _validar_eliminacion(self, id: int) -> None:
        if self._cotizaciones.leer_historico_por_tipo(id):
            raise ValueError(
                "No se puede eliminar un tipo que tiene cotizaciones cargadas."
            )


class LibroService(ServicioCrud[Libro]):
    """Lógica de los libros."""

    entidad = "el libro"

    def __init__(
        self,
        repositorio: IRepositorio[Libro],
        precios: RepositorioPrecio,
        stock: IRepositorioStock,
    ) -> None:
        super().__init__(repositorio)
        self._precios = precios
        self._stock = stock

    def buscar_por_titulo(self, texto: str) -> List[Libro]:
        texto = texto.lower()
        return [
            libro for libro in self.listar() if texto in libro.titulo.lower()
        ]

    def _validar(self, entidad: Libro) -> None:
        for libro in self.listar():
            if libro.id != entidad.id and libro.isbn == entidad.isbn:
                raise ValueError(
                    f"Ya existe un libro con el ISBN {entidad.isbn}."
                )

    def eliminar(self, id: int) -> None:
        """Elimina el libro junto con sus precios y su stock."""
        self.buscar(id)
        for precio in self._precios.leer_por_libro(id):
            self._precios.eliminar(precio.id)
        self._stock.eliminar(id)
        self._repositorio.eliminar(id)


class PrecioService(ServicioCrud[Precio]):
    """Lógica de los precios.

    Un libro tiene como máximo un precio por moneda.
    """

    entidad = "el precio"

    def __init__(self, repositorio: RepositorioPrecio) -> None:
        super().__init__(repositorio)
        self._precios = repositorio

    def precios_de_libro(self, libro_id: int) -> List[Precio]:
        return self._precios.leer_por_libro(libro_id)

    def _validar(self, entidad: Precio) -> None:
        for precio in self.precios_de_libro(entidad.libro.id):
            if (
                precio.id != entidad.id
                and precio.moneda.id == entidad.moneda.id
            ):
                raise ValueError(
                    "El libro ya tiene un precio en "
                    f"{entidad.moneda.codigo}, modificá ese."
                )


class StockService:
    """Lógica del stock de los libros."""

    def __init__(
        self, repositorio: IRepositorioStock, libros: IRepositorio[Libro]
    ) -> None:
        self._repositorio = repositorio
        self._libros = libros

    def listar(self) -> List[Stock]:
        return self._repositorio.leer_todos()

    def buscar(self, libro_id: int) -> Stock:
        """Devuelve el stock de un libro.

        Raises:
            ValueError: Si el libro no tiene stock cargado.
        """
        stock = self._repositorio.leer_por_libro(libro_id)
        if stock is None:
            raise ValueError(f"El libro {libro_id} no tiene stock cargado.")
        return stock

    def crear(
        self, libro_id: int, cantidad: int, cantidad_minima: int
    ) -> Stock:
        libro = self._libros.leer_por_id(libro_id)
        if libro is None:
            raise ValueError(f"No existe un libro con id {libro_id}.")
        return self._repositorio.crear(Stock(libro, cantidad, cantidad_minima))

    def actualizar(
        self, libro_id: int, cantidad: int, cantidad_minima: int
    ) -> Stock:
        stock = self.buscar(libro_id)
        nuevo = Stock(stock.libro, cantidad, cantidad_minima)
        return self._repositorio.actualizar(nuevo)

    def eliminar(self, libro_id: int) -> None:
        if not self._repositorio.eliminar(libro_id):
            raise ValueError(f"El libro {libro_id} no tiene stock cargado.")

    def reponer(self, libro_id: int, cantidad: int) -> Stock:
        """Suma unidades al stock de un libro, por ejemplo por un pedido.

        Args:
            libro_id (int): Id del libro.
            cantidad (int): Unidades que ingresan, debe ser mayor a cero.

        Returns:
            Stock: El stock actualizado.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad a reponer debe ser mayor a cero.")
        stock = self.buscar(libro_id)
        nuevo = Stock(
            stock.libro, stock.cantidad + cantidad, stock.cantidad_minima
        )
        return self._repositorio.actualizar(nuevo)

    def descontar(self, libro_id: int, cantidad: int) -> Stock:
        """Resta unidades del stock de un libro (por ejemplo por una venta).

        Args:
            libro_id (int): Id del libro.
            cantidad (int): Unidades que salen, debe ser mayor a cero.

        Returns:
            Stock: El stock actualizado.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad a descontar debe ser mayor a cero.")
        stock = self.buscar(libro_id)
        if cantidad > stock.cantidad:
            raise ValueError(
                f"No hay suficiente stock del libro {libro_id}: "
                f"hay {stock.cantidad} y se quieren descontar {cantidad}."
            )
        nuevo = Stock(
            stock.libro, stock.cantidad - cantidad, stock.cantidad_minima
        )
        return self._repositorio.actualizar(nuevo)


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


class ReporteService:
    """Reportes del sistema."""

    def __init__(
        self,
        libros: LibroService,
        stock: StockService,
        cotizador: CotizadorService,
    ) -> None:
        self._libros = libros
        self._stock = stock
        self._cotizador = cotizador

    def catalogo_en_pesos(
        self, tipo_id: int
    ) -> List[tuple[Libro, Optional[float]]]:
        """Lista los libros con su precio en pesos según un tipo de dólar."""
        return [
            (libro, self._cotizador.precio_en_pesos(libro.id, tipo_id))
            for libro in self._libros.listar()
        ]

    def stock_bajo(self) -> List[Stock]:
        """Devuelve los libros cuya cantidad está en el mínimo o por debajo.

        Returns:
            List[Stock]: Registros de stock con cantidad <= cantidad_minima,
            ordenados de menor a mayor cantidad.
        """
        bajos = [
            stock
            for stock in self._stock.listar()
            if stock.cantidad <= stock.cantidad_minima
        ]
        return sorted(bajos, key=lambda stock: stock.cantidad)


class Servicios:
    """Crea todos los servicios a partir de los repositorios."""

    def __init__(
        self, repositorios: Repositorios, proveedor: ProveedorCotizaciones
    ) -> None:
        self.generos = GeneroService(repositorios.generos, repositorios.libros)
        self.editoriales = EditorialService(
            repositorios.editoriales, repositorios.libros
        )
        self.monedas = MonedaService(
            repositorios.monedas, repositorios.precios
        )
        self.tipos_cotizacion = TipoCotizacionService(
            repositorios.tipos_cotizacion, repositorios.cotizaciones
        )
        self.libros = LibroService(
            repositorios.libros, repositorios.precios, repositorios.stock
        )
        self.precios = PrecioService(repositorios.precios)
        self.stock = StockService(repositorios.stock, repositorios.libros)
        self.cotizaciones = CotizacionService(
            repositorios.cotizaciones, self.tipos_cotizacion, proveedor
        )
        self.cotizador = CotizadorService(
            self.precios, self.cotizaciones, self.tipos_cotizacion
        )
        self.reportes = ReporteService(self.libros, self.stock, self.cotizador)
