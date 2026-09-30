"""Entidades del sistema de gestión de la librería."""

import abc
import datetime


def _validar_texto(valor: str, campo: str) -> str:
    """Valida que un texto no esté vacío y lo devuelve sin espacios extra.

    Args:
        valor (str): Texto a validar.
        campo (str): Nombre del campo, se usa en el mensaje de error.

    Returns:
        str: El texto sin espacios al principio ni al final.
    """
    valor = str(valor).strip()
    if not valor:
        raise ValueError(f"El campo {campo} es obligatorio.")
    return valor


def _validar_positivo(valor: float, campo: str) -> float:
    """Valida que un número sea mayor a cero."""
    valor = float(valor)
    if valor <= 0:
        raise ValueError(f"El campo {campo} debe ser mayor a cero.")
    return valor


class EntidadBase(abc.ABC):
    """Clase base de las entidades que se identifican por un id.

    El id 0 indica que la entidad todavía no fue guardada; el repositorio
    le asigna uno nuevo al crearla.
    """

    def __init__(self, id: int = 0) -> None:
        self.id = id

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, valor: int) -> None:
        valor = int(valor)
        if valor < 0:
            raise ValueError("El id no puede ser negativo.")
        self._id = valor

    def __eq__(self, otro: object) -> bool:
        return type(self) is type(otro) and self.id == otro.id

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.id))


class Genero(EntidadBase):
    """Categoría literaria a la que pertenece un libro."""

    def __init__(self, id: int, nombre: str, descripcion: str = "") -> None:
        super().__init__(id)
        self.nombre = nombre
        self.descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = _validar_texto(valor, "nombre")

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        self._descripcion = str(valor).strip()

    def __str__(self) -> str:
        return self.nombre


class Editorial(EntidadBase):
    """Proveedor o distribuidora que le vende los libros a la librería."""

    def __init__(
        self, id: int, nombre: str, pais: str, sitio_web: str = ""
    ) -> None:
        super().__init__(id)
        self.nombre = nombre
        self.pais = pais
        self.sitio_web = sitio_web

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = _validar_texto(valor, "nombre")

    @property
    def pais(self) -> str:
        return self._pais

    @pais.setter
    def pais(self, valor: str) -> None:
        self._pais = _validar_texto(valor, "país")

    @property
    def sitio_web(self) -> str:
        return self._sitio_web

    @sitio_web.setter
    def sitio_web(self, valor: str) -> None:
        self._sitio_web = str(valor).strip()

    def __str__(self) -> str:
        return self.nombre


class Moneda(EntidadBase):
    """Moneda en la que se puede expresar un precio.

    El código usa el formato ISO 4217: tres letras (ARS, USD, EUR).
    """

    def __init__(
        self, id: int, codigo: str, nombre: str, simbolo: str
    ) -> None:
        super().__init__(id)
        self.codigo = codigo
        self.nombre = nombre
        self.simbolo = simbolo

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        valor = _validar_texto(valor, "código").upper()
        if len(valor) != 3 or not valor.isalpha():
            raise ValueError(
                "El código de moneda debe tener 3 letras, por ejemplo ARS."
            )
        self._codigo = valor

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = _validar_texto(valor, "nombre")

    @property
    def simbolo(self) -> str:
        return self._simbolo

    @simbolo.setter
    def simbolo(self, valor: str) -> None:
        self._simbolo = _validar_texto(valor, "símbolo")

    def __str__(self) -> str:
        return f"{self.codigo} ({self.simbolo})"


class TipoCotizacion(EntidadBase):
    """Tipo de cotización del dólar (Oficial, Blue, MEP, etc.).

    El código coincide con el que usa DolarApi para identificar cada
    cotización.
    """

    def __init__(self, id: int, codigo: str, nombre: str) -> None:
        super().__init__(id)
        self.codigo = codigo
        self.nombre = nombre

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        self._codigo = _validar_texto(valor, "código").lower()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = _validar_texto(valor, "nombre")

    def __str__(self) -> str:
        return self.nombre


class Libro(EntidadBase):
    """Título del catálogo de la librería."""

    def __init__(
        self,
        id: int,
        isbn: str,
        titulo: str,
        autor: str,
        editorial: Editorial,
        genero: Genero,
        anio_publicacion: int,
    ) -> None:
        super().__init__(id)
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.editorial = editorial
        self.genero = genero
        self.anio_publicacion = anio_publicacion

    @property
    def isbn(self) -> str:
        return self._isbn

    @isbn.setter
    def isbn(self, valor: str) -> None:
        valor = _validar_texto(valor, "ISBN").replace("-", "").replace(" ", "")
        if not valor.isdigit() or len(valor) not in (10, 13):
            raise ValueError("El ISBN debe tener 10 o 13 dígitos.")
        self._isbn = valor

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        self._titulo = _validar_texto(valor, "título")

    @property
    def autor(self) -> str:
        return self._autor

    @autor.setter
    def autor(self, valor: str) -> None:
        self._autor = _validar_texto(valor, "autor")

    @property
    def editorial(self) -> Editorial:
        return self._editorial

    @editorial.setter
    def editorial(self, valor: Editorial) -> None:
        if not isinstance(valor, Editorial):
            raise ValueError("El libro debe tener una editorial válida.")
        self._editorial = valor

    @property
    def genero(self) -> Genero:
        return self._genero

    @genero.setter
    def genero(self, valor: Genero) -> None:
        if not isinstance(valor, Genero):
            raise ValueError("El libro debe tener un género válido.")
        self._genero = valor

    @property
    def anio_publicacion(self) -> int:
        return self._anio_publicacion

    @anio_publicacion.setter
    def anio_publicacion(self, valor: int) -> None:
        valor = int(valor)
        if valor < 1450 or valor > datetime.date.today().year:
            raise ValueError("El año de publicación no es válido.")
        self._anio_publicacion = valor

    def __str__(self) -> str:
        return f"{self.titulo} - {self.autor}"


class Precio(EntidadBase):
    """Precio de un libro expresado en una moneda."""

    def __init__(
        self, id: int, libro: Libro, moneda: Moneda, monto: float
    ) -> None:
        super().__init__(id)
        self.libro = libro
        self.moneda = moneda
        self.monto = monto

    @property
    def libro(self) -> Libro:
        return self._libro

    @libro.setter
    def libro(self, valor: Libro) -> None:
        if not isinstance(valor, Libro):
            raise ValueError("El precio debe estar asociado a un libro.")
        self._libro = valor

    @property
    def moneda(self) -> Moneda:
        return self._moneda

    @moneda.setter
    def moneda(self, valor: Moneda) -> None:
        if not isinstance(valor, Moneda):
            raise ValueError("El precio debe tener una moneda válida.")
        self._moneda = valor

    @property
    def monto(self) -> float:
        return self._monto

    @monto.setter
    def monto(self, valor: float) -> None:
        self._monto = round(_validar_positivo(valor, "monto"), 2)

    def __str__(self) -> str:
        return f"{self.moneda.simbolo} {self.monto:,.2f}"


class Stock:
    """Cantidad disponible de un libro. Se identifica por el libro."""

    def __init__(
        self, libro: Libro, cantidad: int, cantidad_minima: int = 5
    ) -> None:
        self.libro = libro
        self.cantidad = cantidad
        self.cantidad_minima = cantidad_minima

    @property
    def libro(self) -> Libro:
        return self._libro

    @libro.setter
    def libro(self, valor: Libro) -> None:
        if not isinstance(valor, Libro):
            raise ValueError("El stock debe estar asociado a un libro.")
        self._libro = valor

    @property
    def libro_id(self) -> int:
        return self._libro.id

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        valor = int(valor)
        if valor < 0:
            raise ValueError("La cantidad en stock no puede ser negativa.")
        self._cantidad = valor

    @property
    def cantidad_minima(self) -> int:
        return self._cantidad_minima

    @cantidad_minima.setter
    def cantidad_minima(self, valor: int) -> None:
        valor = int(valor)
        if valor < 0:
            raise ValueError("La cantidad mínima no puede ser negativa.")
        self._cantidad_minima = valor

    def __str__(self) -> str:
        return f"{self.libro.titulo}: {self.cantidad} unidades"


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
