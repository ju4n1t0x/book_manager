"""Persistencia de las entidades en archivos CSV."""

import abc
import csv
import datetime
from pathlib import Path
from typing import Generic, Iterator, List, Optional, TypeVar

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

DIRECTORIO_DATOS = Path(__file__).resolve().parent.parent / "migrations" / "csv"

T = TypeVar("T", bound=EntidadBase)


class IRepositorio(abc.ABC, Generic[T]):
    """Interfaz para repositorios que manejan entidades con operaciones CRUD básicas."""

    @abc.abstractmethod
    def crear(self, entidad: T) -> T:
        """Crea una nueva entidad en el repositorio.

        Args:
            entidad (T): La entidad a crear.

        Returns:
            T: La entidad creada.

        Raises:
            ValueError: Si ya existe una entidad con el mismo ID.
        """
        pass

    @abc.abstractmethod
    def leer_por_id(self, id: int) -> Optional[T]:
        """Lee una entidad del repositorio por su ID.

        Args:
            id (int): El ID de la entidad a leer.

        Returns:
            Optional[T]: La entidad si se encuentra, None en caso contrario.
        """
        pass

    @abc.abstractmethod
    def leer_todos(self) -> List[T]:
        """Lee todas las entidades del repositorio.

        Returns:
            List[T]: Una lista de todas las entidades.
        """
        pass

    @abc.abstractmethod
    def actualizar(self, entidad: T) -> T:
        """Actualiza una entidad existente en el repositorio.

        Args:
            entidad (T): La entidad a actualizar (debe tener un ID existente).

        Returns:
            T: La entidad actualizada.

        Raises:
            ValueError: Si no se encuentra la entidad para actualizar.
        """
        pass

    @abc.abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina una entidad del repositorio por su ID.

        Args:
            id (int): El ID de la entidad a eliminar.

        Returns:
            bool: True si la entidad fue eliminada, False si no se encontró.
        """
        pass


class IRepositorioStock(abc.ABC):
    """Interfaz para repositorios del tipo Stock."""

    @abc.abstractmethod
    def crear(self, stock: Stock) -> Stock:
        """Crea un nuevo registro de stock.

        Args:
            stock (Stock): El objeto Stock a crear.

        Returns:
            Stock: El objeto Stock creado.

        Raises:
            ValueError: Si ya existe un registro de stock para el mismo libro.
        """
        pass

    @abc.abstractmethod
    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        """Lee un registro de stock por ID de libro.

        Args:
            libro_id (int): El ID del libro asociado al stock.

        Returns:
            Optional[Stock]: El objeto Stock si se encuentra, None en caso contrario.
        """
        pass

    @abc.abstractmethod
    def actualizar(self, stock: Stock) -> Stock:
        """Actualiza un registro de stock existente.

        Args:
            stock (Stock): El objeto Stock a actualizar (debe tener un libro_id existente).

        Returns:
            Stock: El objeto Stock actualizado.

        Raises:
            ValueError: Si no se encuentra el stock para actualizar.
        """
        pass

    @abc.abstractmethod
    def eliminar(self, libro_id: int) -> bool:
        """Elimina un registro de stock por ID de libro.

        Args:
            libro_id (int): El ID del libro asociado al stock a eliminar.

        Returns:
            bool: True si el stock fue eliminado, False si no se encontró.
        """
        pass


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
            tipo_id (int): El ID del tipo de cotización (e.g., 'Oficial', 'Blue').
            fecha (datetime.date): La fecha de la cotización.

        Returns:
            Optional[CotizacionDolar]: La cotización si se encuentra, None en caso contrario.
        """
        pass

    @abc.abstractmethod
    def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
        """Lee el histórico de cotizaciones para un tipo específico.

        Args:
            tipo_id (int): El ID del tipo de cotización.

        Returns:
            List[CotizacionDolar]: Una lista de cotizaciones históricas para el tipo dado.
        """
        pass

    @abc.abstractmethod
    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        """Actualiza una cotización de dólar existente.

        Args:
            cotizacion (CotizacionDolar): El objeto CotizacionDolar a actualizar.

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


class ArchivoCSV:
    """Lectura y escritura de un archivo CSV con encabezado."""

    def __init__(self, ruta: Path, campos: List[str]) -> None:
        self._ruta = ruta
        self._campos = campos

    def leer(self) -> Iterator[dict[str, str]]:
        """Devuelve las filas del archivo de a una.

        Returns:
            Iterator[dict[str, str]]: Cada fila como diccionario campo -> valor.
        """
        if not self._ruta.exists():
            return
        with open(self._ruta, "r", encoding="utf-8", newline="") as archivo:
            for fila in csv.DictReader(archivo):
                yield fila

    def escribir(self, filas: List[dict]) -> None:
        """Reescribe el archivo completo con las filas recibidas."""
        self._ruta.parent.mkdir(parents=True, exist_ok=True)
        with open(self._ruta, "w", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=self._campos)
            escritor.writeheader()
            escritor.writerows(filas)


class RepositorioCSV(IRepositorio[T]):
    """Repositorio genérico que guarda las entidades en un archivo CSV.

    Mantiene las entidades en memoria y reescribe el archivo en cada cambio.
    Cada repositorio concreto indica los campos del archivo y cómo pasar
    una entidad a una fila y viceversa.
    """

    campos: List[str] = []

    def __init__(self, ruta: Path) -> None:
        self._archivo = ArchivoCSV(ruta, self.campos)
        self._entidades: dict[int, T] = {}
        for fila in self._archivo.leer():
            entidad = self._desde_fila(fila)
            self._entidades[entidad.id] = entidad

    @abc.abstractmethod
    def _a_fila(self, entidad: T) -> dict:
        """Convierte la entidad en una fila del CSV."""

    @abc.abstractmethod
    def _desde_fila(self, fila: dict[str, str]) -> T:
        """Arma la entidad a partir de una fila del CSV."""

    def _guardar(self) -> None:
        self._archivo.escribir([self._a_fila(e) for e in self._entidades.values()])

    def _proximo_id(self) -> int:
        return max(self._entidades, default=0) + 1

    def crear(self, entidad: T) -> T:
        if entidad.id == 0:
            entidad.id = self._proximo_id()
        if entidad.id in self._entidades:
            raise ValueError(f"Ya existe un registro con id {entidad.id}.")
        self._entidades[entidad.id] = entidad
        self._guardar()
        return entidad

    def leer_por_id(self, id: int) -> Optional[T]:
        return self._entidades.get(id)

    def leer_todos(self) -> List[T]:
        return list(self._entidades.values())

    def actualizar(self, entidad: T) -> T:
        actual = self._entidades.get(entidad.id)
        if actual is None:
            raise ValueError(f"No existe un registro con id {entidad.id}.")
        # Se copian los datos sobre el objeto que ya existe, así los objetos que
        # lo referencian (por ejemplo un libro con su género) ven el cambio.
        if actual is not entidad:
            vars(actual).update(vars(entidad))
        self._guardar()
        return actual

    def eliminar(self, id: int) -> bool:
        if id not in self._entidades:
            return False
        del self._entidades[id]
        self._guardar()
        return True


class RepositorioGenero(RepositorioCSV[Genero]):
    """Repositorio de géneros."""

    campos = ["id", "nombre", "descripcion"]

    def _a_fila(self, entidad: Genero) -> dict:
        return {"id": entidad.id, "nombre": entidad.nombre, "descripcion": entidad.descripcion}

    def _desde_fila(self, fila: dict[str, str]) -> Genero:
        return Genero(int(fila["id"]), fila["nombre"], fila["descripcion"])


class RepositorioEditorial(RepositorioCSV[Editorial]):
    """Repositorio de editoriales."""

    campos = ["id", "nombre", "pais", "sitio_web"]

    def _a_fila(self, entidad: Editorial) -> dict:
        return {
            "id": entidad.id,
            "nombre": entidad.nombre,
            "pais": entidad.pais,
            "sitio_web": entidad.sitio_web,
        }

    def _desde_fila(self, fila: dict[str, str]) -> Editorial:
        return Editorial(int(fila["id"]), fila["nombre"], fila["pais"], fila["sitio_web"])


class RepositorioMoneda(RepositorioCSV[Moneda]):
    """Repositorio de monedas."""

    campos = ["id", "codigo", "nombre", "simbolo"]

    def _a_fila(self, entidad: Moneda) -> dict:
        return {
            "id": entidad.id,
            "codigo": entidad.codigo,
            "nombre": entidad.nombre,
            "simbolo": entidad.simbolo,
        }

    def _desde_fila(self, fila: dict[str, str]) -> Moneda:
        return Moneda(int(fila["id"]), fila["codigo"], fila["nombre"], fila["simbolo"])


class RepositorioTipoCotizacion(RepositorioCSV[TipoCotizacion]):
    """Repositorio de tipos de cotización."""

    campos = ["id", "codigo", "nombre"]

    def _a_fila(self, entidad: TipoCotizacion) -> dict:
        return {"id": entidad.id, "codigo": entidad.codigo, "nombre": entidad.nombre}

    def _desde_fila(self, fila: dict[str, str]) -> TipoCotizacion:
        return TipoCotizacion(int(fila["id"]), fila["codigo"], fila["nombre"])


class RepositorioLibro(RepositorioCSV[Libro]):
    """Repositorio de libros.

    En el archivo se guardan los ids de la editorial y el género; al leer
    se buscan en sus repositorios para armar el libro completo.
    """

    campos = ["id", "isbn", "titulo", "autor", "editorial_id", "genero_id", "anio_publicacion"]

    def __init__(
        self,
        ruta: Path,
        editoriales: RepositorioEditorial,
        generos: RepositorioGenero,
    ) -> None:
        self._editoriales = editoriales
        self._generos = generos
        super().__init__(ruta)

    def _a_fila(self, entidad: Libro) -> dict:
        return {
            "id": entidad.id,
            "isbn": entidad.isbn,
            "titulo": entidad.titulo,
            "autor": entidad.autor,
            "editorial_id": entidad.editorial.id,
            "genero_id": entidad.genero.id,
            "anio_publicacion": entidad.anio_publicacion,
        }

    def _desde_fila(self, fila: dict[str, str]) -> Libro:
        editorial = self._editoriales.leer_por_id(int(fila["editorial_id"]))
        genero = self._generos.leer_por_id(int(fila["genero_id"]))
        if editorial is None or genero is None:
            raise ValueError(
                f"El libro {fila['id']} tiene una editorial o un género que no existe."
            )
        return Libro(
            int(fila["id"]),
            fila["isbn"],
            fila["titulo"],
            fila["autor"],
            editorial,
            genero,
            int(fila["anio_publicacion"]),
        )


class RepositorioPrecio(RepositorioCSV[Precio]):
    """Repositorio de precios."""

    campos = ["id", "libro_id", "moneda_id", "monto"]

    def __init__(self, ruta: Path, libros: RepositorioLibro, monedas: RepositorioMoneda) -> None:
        self._libros = libros
        self._monedas = monedas
        super().__init__(ruta)

    def _a_fila(self, entidad: Precio) -> dict:
        return {
            "id": entidad.id,
            "libro_id": entidad.libro.id,
            "moneda_id": entidad.moneda.id,
            "monto": entidad.monto,
        }

    def _desde_fila(self, fila: dict[str, str]) -> Precio:
        libro = self._libros.leer_por_id(int(fila["libro_id"]))
        moneda = self._monedas.leer_por_id(int(fila["moneda_id"]))
        if libro is None or moneda is None:
            raise ValueError(f"El precio {fila['id']} tiene un libro o una moneda que no existe.")
        return Precio(int(fila["id"]), libro, moneda, float(fila["monto"]))

    def leer_por_libro(self, libro_id: int) -> List[Precio]:
        """Devuelve los precios cargados para un libro."""
        return [p for p in self._entidades.values() if p.libro.id == libro_id]


class RepositorioStock(IRepositorioStock):
    """Repositorio de stock guardado en CSV. La clave es el id del libro."""

    campos = ["libro_id", "cantidad", "cantidad_minima"]

    def __init__(self, ruta: Path, libros: RepositorioLibro) -> None:
        self._libros = libros
        self._archivo = ArchivoCSV(ruta, self.campos)
        self._stock: dict[int, Stock] = {}
        for fila in self._archivo.leer():
            stock = self._desde_fila(fila)
            self._stock[stock.libro_id] = stock

    def _a_fila(self, stock: Stock) -> dict:
        return {
            "libro_id": stock.libro_id,
            "cantidad": stock.cantidad,
            "cantidad_minima": stock.cantidad_minima,
        }

    def _desde_fila(self, fila: dict[str, str]) -> Stock:
        libro = self._libros.leer_por_id(int(fila["libro_id"]))
        if libro is None:
            raise ValueError(f"Hay stock cargado para el libro {fila['libro_id']} que no existe.")
        return Stock(libro, int(fila["cantidad"]), int(fila["cantidad_minima"]))

    def _guardar(self) -> None:
        self._archivo.escribir([self._a_fila(s) for s in self._stock.values()])

    def crear(self, stock: Stock) -> Stock:
        if stock.libro_id in self._stock:
            raise ValueError(f"Ya hay stock cargado para el libro {stock.libro_id}.")
        self._stock[stock.libro_id] = stock
        self._guardar()
        return stock

    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        return self._stock.get(libro_id)

    def leer_todos(self) -> List[Stock]:
        """Devuelve el stock de todos los libros."""
        return list(self._stock.values())

    def actualizar(self, stock: Stock) -> Stock:
        if stock.libro_id not in self._stock:
            raise ValueError(f"No hay stock cargado para el libro {stock.libro_id}.")
        self._stock[stock.libro_id] = stock
        self._guardar()
        return stock

    def eliminar(self, libro_id: int) -> bool:
        if libro_id not in self._stock:
            return False
        del self._stock[libro_id]
        self._guardar()
        return True


class RepositorioCotizacionDolar(IRepositorioCotizacionDolar):
    """Repositorio de cotizaciones guardado en CSV. La clave es (tipo, fecha)."""

    campos = ["tipo_id", "fecha", "compra", "venta"]

    def __init__(self, ruta: Path, tipos: RepositorioTipoCotizacion) -> None:
        self._tipos = tipos
        self._archivo = ArchivoCSV(ruta, self.campos)
        self._cotizaciones: dict[tuple[int, datetime.date], CotizacionDolar] = {}
        for fila in self._archivo.leer():
            cotizacion = self._desde_fila(fila)
            self._cotizaciones[(cotizacion.tipo_id, cotizacion.fecha)] = cotizacion

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
            raise ValueError(f"Hay cotizaciones de un tipo que no existe ({fila['tipo_id']}).")
        fecha = datetime.date.fromisoformat(fila["fecha"])
        return CotizacionDolar(tipo, fecha, float(fila["compra"]), float(fila["venta"]))

    def _guardar(self) -> None:
        ordenadas = sorted(self._cotizaciones.values(), key=lambda c: (c.tipo_id, c.fecha))
        self._archivo.escribir([self._a_fila(c) for c in ordenadas])

    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        clave = (cotizacion.tipo_id, cotizacion.fecha)
        if clave in self._cotizaciones:
            raise ValueError(
                f"Ya existe una cotización {cotizacion.tipo.nombre} del {cotizacion.fecha}."
            )
        self._cotizaciones[clave] = cotizacion
        self._guardar()
        return cotizacion

    def leer_por_tipo_y_fecha(
        self, tipo_id: int, fecha: datetime.date
    ) -> Optional[CotizacionDolar]:
        return self._cotizaciones.get((tipo_id, fecha))

    def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
        historico = [c for c in self._cotizaciones.values() if c.tipo_id == tipo_id]
        return sorted(historico, key=lambda c: c.fecha)

    def leer_todos(self) -> List[CotizacionDolar]:
        """Devuelve todas las cotizaciones ordenadas por tipo y fecha."""
        return sorted(self._cotizaciones.values(), key=lambda c: (c.tipo_id, c.fecha))

    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        clave = (cotizacion.tipo_id, cotizacion.fecha)
        if clave not in self._cotizaciones:
            raise ValueError(
                f"No existe una cotización {cotizacion.tipo.nombre} del {cotizacion.fecha}."
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


class Repositorios:
    """Crea todos los repositorios del sistema en el orden correcto.

    El orden importa porque los libros necesitan los géneros y editoriales,
    los precios necesitan los libros y las monedas, etc.
    """

    def __init__(self, directorio: Path = DIRECTORIO_DATOS) -> None:
        self.generos = RepositorioGenero(directorio / "generos.csv")
        self.editoriales = RepositorioEditorial(directorio / "editoriales.csv")
        self.monedas = RepositorioMoneda(directorio / "monedas.csv")
        self.tipos_cotizacion = RepositorioTipoCotizacion(directorio / "tipos_cotizacion.csv")
        self.libros = RepositorioLibro(directorio / "libros.csv", self.editoriales, self.generos)
        self.precios = RepositorioPrecio(directorio / "precios.csv", self.libros, self.monedas)
        self.stock = RepositorioStock(directorio / "stock.csv", self.libros)
        self.cotizaciones = RepositorioCotizacionDolar(
            directorio / "cotizaciones.csv", self.tipos_cotizacion
        )
