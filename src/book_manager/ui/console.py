"""Menús de consola del sistema."""

import datetime
import functools
from enum import IntEnum
from typing import Any, Callable, Optional

from book_manager.entities.entities import (
    Editorial,
    Genero,
    Libro,
    Moneda,
    Precio,
    TipoCotizacion,
)
from book_manager.services.services import ServicioCrud, Servicios


def manejar_errores(funcion: Callable) -> Callable:
    """Decorador que muestra los errores sin cortar el programa."""

    @functools.wraps(funcion)
    def envoltura(*args: Any, **kwargs: Any) -> Any:
        try:
            return funcion(*args, **kwargs)
        except ValueError as error:
            print(f"\nError: {error}")
        except NotImplementedError:
            print("\nEsta opción todavía no está disponible.")
        return None

    return envoltura


def pedir_texto(
    mensaje: str, actual: Optional[str] = None, obligatorio: bool = True
) -> str:
    """Pide un texto por teclado.

    Args:
        mensaje (str): Texto que se muestra al usuario.
        actual (Optional[str]): Valor actual; si se pasa, con Enter se
            mantiene.
        obligatorio (bool): Si es False se acepta un texto vacío.

    Returns:
        str: El texto ingresado.
    """
    sufijo = f" [{actual}]" if actual is not None else ""
    while True:
        valor = input(f"{mensaje}{sufijo}: ").strip()
        if not valor and actual is not None:
            return actual
        if valor or not obligatorio:
            return valor
        print("Este dato es obligatorio.")


def pedir_entero(mensaje: str, actual: Optional[int] = None) -> int:
    """Pide un número entero y repregunta si lo ingresado no es válido."""
    while True:
        valor = pedir_texto(mensaje, None if actual is None else str(actual))
        try:
            return int(valor)
        except ValueError:
            print("Ingresá un número entero.")


def pedir_decimal(mensaje: str, actual: Optional[float] = None) -> float:
    """Pide un número con decimales. Acepta coma o punto."""
    while True:
        valor = pedir_texto(mensaje, None if actual is None else str(actual))
        try:
            return float(valor.replace(",", "."))
        except ValueError:
            print("Ingresá un número, por ejemplo 1250.50")


def pedir_fecha(
    mensaje: str, actual: Optional[datetime.date] = None
) -> datetime.date:
    """Pide una fecha con formato AAAA-MM-DD.

    Si no hay valor actual, con Enter se toma la fecha de hoy.
    """
    actual = actual or datetime.date.today()
    while True:
        valor = pedir_texto(f"{mensaje} (AAAA-MM-DD)", actual.isoformat())
        try:
            return datetime.date.fromisoformat(valor)
        except ValueError:
            print("La fecha debe tener el formato AAAA-MM-DD.")


def confirmar(mensaje: str) -> bool:
    return input(f"{mensaje} (s/n): ").strip().lower() == "s"


def mostrar_tabla(encabezados: list[str], filas: list[list[Any]]) -> None:
    """Imprime una tabla con columnas alineadas."""
    if not filas:
        print("\nNo hay registros para mostrar.")
        return
    filas_texto = [[str(valor) for valor in fila] for fila in filas]
    anchos = [
        max(len(encabezados[i]), *(len(fila[i]) for fila in filas_texto))
        for i in range(len(encabezados))
    ]
    print()
    print(" | ".join(e.ljust(a) for e, a in zip(encabezados, anchos)))
    print("-+-".join("-" * a for a in anchos))
    for fila in filas_texto:
        print(" | ".join(v.ljust(a) for v, a in zip(fila, anchos)))


def formato_pesos(monto: Optional[float]) -> str:
    return "sin datos" if monto is None else f"$ {monto:,.2f}"


class OpcionPrincipal(IntEnum):
    SALIR = 0
    LIBROS = 1
    GENEROS = 2
    EDITORIALES = 3
    MONEDAS = 4
    PRECIOS = 5
    STOCK = 6
    TIPOS_COTIZACION = 7
    COTIZACIONES = 8
    REPORTES = 9


class Consola:
    """Interfaz de consola que opera con los servicios del sistema."""

    def __init__(self, servicios: Servicios) -> None:
        self._s = servicios

    def iniciar(self) -> None:
        print("\n==============================")
        print("   BOOK MANAGER - Librería")
        print("==============================")
        self._actualizar_cotizaciones()
        try:
            self._menu_principal()
        except (KeyboardInterrupt, EOFError):
            pass
        print("\nHasta luego.")

    def _menu_principal(self) -> None:
        while True:
            print("\n--- Menú principal ---")
            print("1. Libros")
            print("2. Géneros")
            print("3. Editoriales")
            print("4. Monedas")
            print("5. Precios")
            print("6. Stock")
            print("7. Tipos de cotización")
            print("8. Cotizaciones del dólar")
            print("9. Reportes")
            print("0. Salir")
            try:
                opcion = OpcionPrincipal(int(input("Opción: ")))
            except ValueError:
                print("Opción inválida.")
                continue

            match opcion:
                case OpcionPrincipal.LIBROS:
                    self._menu_libros()
                case OpcionPrincipal.GENEROS:
                    self._menu_generos()
                case OpcionPrincipal.EDITORIALES:
                    self._menu_editoriales()
                case OpcionPrincipal.MONEDAS:
                    self._menu_monedas()
                case OpcionPrincipal.PRECIOS:
                    self._menu_precios()
                case OpcionPrincipal.STOCK:
                    self._menu_stock()
                case OpcionPrincipal.TIPOS_COTIZACION:
                    self._menu_tipos_cotizacion()
                case OpcionPrincipal.COTIZACIONES:
                    self._menu_cotizaciones()
                case OpcionPrincipal.REPORTES:
                    self._menu_reportes()
                case OpcionPrincipal.SALIR:
                    return

    def _menu_crud(
        self,
        titulo: str,
        listar: Callable,
        alta: Callable,
        modificar: Callable,
        baja: Callable,
        extras: Optional[list[tuple[str, Callable]]] = None,
    ) -> None:
        """Menú con las opciones de CRUD de una entidad.

        Args:
            titulo (str): Nombre del menú.
            listar, alta, modificar, baja (Callable): Métodos de cada opción.
            extras (Optional[list[tuple[str, Callable]]]): Opciones adicionales
                (texto, método) que se muestran a partir del número 5.
        """
        extras = extras or []
        while True:
            print(f"\n--- {titulo} ---")
            print("1. Listar")
            print("2. Alta")
            print("3. Modificar")
            print("4. Baja")
            for numero, (texto, _) in enumerate(extras, start=5):
                print(f"{numero}. {texto}")
            print("0. Volver")
            opcion = input("Opción: ").strip()

            match opcion:
                case "1":
                    listar()
                case "2":
                    alta()
                case "3":
                    modificar()
                case "4":
                    baja()
                case "0":
                    return
                case _ if opcion.isdigit() and 5 <= int(opcion) < 5 + len(
                    extras
                ):
                    extras[int(opcion) - 5][1]()
                case _:
                    print("Opción inválida.")

    @staticmethod
    def _elegir(
        servicio: ServicioCrud, titulo: str, actual: Optional[Any] = None
    ) -> Any:
        """Muestra los registros de un servicio y pide el id de uno."""
        print(f"\nOpciones de {titulo.lower()}:")
        for entidad in servicio.listar():
            print(f"  {entidad.id}. {entidad}")
        id = pedir_entero(
            f"Id de {titulo.lower()}", None if actual is None else actual.id
        )
        return servicio.buscar(id)

    def _menu_libros(self) -> None:
        self._menu_crud(
            "Libros",
            self._listar_libros,
            self._alta_libro,
            self._modificar_libro,
            self._baja_libro,
            [("Buscar por título", self._buscar_libros)],
        )

    @staticmethod
    def _tabla_libros(libros: list[Libro]) -> None:
        mostrar_tabla(
            ["Id", "ISBN", "Título", "Autor", "Editorial", "Género", "Año"],
            [
                [
                    libro.id,
                    libro.isbn,
                    libro.titulo,
                    libro.autor,
                    libro.editorial,
                    libro.genero,
                    libro.anio_publicacion,
                ]
                for libro in libros
            ],
        )

    @manejar_errores
    def _listar_libros(self) -> None:
        self._tabla_libros(self._s.libros.listar())

    @manejar_errores
    def _buscar_libros(self) -> None:
        texto = pedir_texto("Texto a buscar en el título")
        self._tabla_libros(self._s.libros.buscar_por_titulo(texto))

    @manejar_errores
    def _alta_libro(self) -> None:
        print("\nNuevo libro")
        isbn = pedir_texto("ISBN")
        titulo = pedir_texto("Título")
        autor = pedir_texto("Autor")
        anio = pedir_entero("Año de publicación")
        editorial = self._elegir(self._s.editoriales, "Editorial")
        genero = self._elegir(self._s.generos, "Género")
        libro = self._s.libros.crear(
            Libro(0, isbn, titulo, autor, editorial, genero, anio)
        )
        print(f"\nLibro creado con id {libro.id}.")

    @manejar_errores
    def _modificar_libro(self) -> None:
        libro = self._s.libros.buscar(pedir_entero("Id del libro a modificar"))
        print("Enter para mantener el valor actual.")
        isbn = pedir_texto("ISBN", libro.isbn)
        titulo = pedir_texto("Título", libro.titulo)
        autor = pedir_texto("Autor", libro.autor)
        anio = pedir_entero("Año de publicación", libro.anio_publicacion)
        editorial = self._elegir(
            self._s.editoriales, "Editorial", libro.editorial
        )
        genero = self._elegir(self._s.generos, "Género", libro.genero)
        self._s.libros.actualizar(
            Libro(libro.id, isbn, titulo, autor, editorial, genero, anio)
        )
        print("\nLibro actualizado.")

    @manejar_errores
    def _baja_libro(self) -> None:
        libro = self._s.libros.buscar(pedir_entero("Id del libro a eliminar"))
        if confirmar(
            f"Se elimina '{libro}' junto con sus precios y stock. ¿Continuar?"
        ):
            self._s.libros.eliminar(libro.id)
            print("\nLibro eliminado.")

    def _menu_generos(self) -> None:
        self._menu_crud(
            "Géneros",
            self._listar_generos,
            self._alta_genero,
            self._modificar_genero,
            self._baja_genero,
        )

    @manejar_errores
    def _listar_generos(self) -> None:
        mostrar_tabla(
            ["Id", "Nombre", "Descripción"],
            [
                [g.id, g.nombre, g.descripcion]
                for g in self._s.generos.listar()
            ],
        )

    @manejar_errores
    def _alta_genero(self) -> None:
        print("\nNuevo género")
        nombre = pedir_texto("Nombre del género")
        descripcion = pedir_texto("Descripción", obligatorio=False)
        genero = self._s.generos.crear(Genero(0, nombre, descripcion))
        print(f"\nGénero creado con id {genero.id}.")

    @manejar_errores
    def _modificar_genero(self) -> None:
        genero = self._s.generos.buscar(
            pedir_entero("Id del género a modificar")
        )
        print("Enter para mantener el valor actual.")
        nombre = pedir_texto("Nombre", genero.nombre)
        descripcion = pedir_texto("Descripción", genero.descripcion)
        self._s.generos.actualizar(Genero(genero.id, nombre, descripcion))
        print("\nGénero actualizado.")

    @manejar_errores
    def _baja_genero(self) -> None:
        genero = self._s.generos.buscar(
            pedir_entero("Id del género a eliminar")
        )
        if confirmar(f"¿Eliminar el género '{genero.nombre}'?"):
            self._s.generos.eliminar(genero.id)
            print("\nGénero eliminado.")

    def _menu_editoriales(self) -> None:
        self._menu_crud(
            "Editoriales",
            self._listar_editoriales,
            self._alta_editorial,
            self._modificar_editorial,
            self._baja_editorial,
        )

    @manejar_errores
    def _listar_editoriales(self) -> None:
        mostrar_tabla(
            ["Id", "Nombre", "País", "Sitio web"],
            [
                [e.id, e.nombre, e.pais, e.sitio_web]
                for e in self._s.editoriales.listar()
            ],
        )

    @manejar_errores
    def _alta_editorial(self) -> None:
        print("\nNueva editorial")
        nombre = pedir_texto("Nombre de la editorial")
        pais = pedir_texto("País")
        sitio_web = pedir_texto("Sitio web", obligatorio=False)
        editorial = self._s.editoriales.crear(
            Editorial(0, nombre, pais, sitio_web)
        )
        print(f"\nEditorial creada con id {editorial.id}.")

    @manejar_errores
    def _modificar_editorial(self) -> None:
        editorial = self._s.editoriales.buscar(
            pedir_entero("Id de la editorial a modificar")
        )
        print("Enter para mantener el valor actual.")
        nombre = pedir_texto("Nombre", editorial.nombre)
        pais = pedir_texto("País", editorial.pais)
        sitio_web = pedir_texto("Sitio web", editorial.sitio_web)
        self._s.editoriales.actualizar(
            Editorial(editorial.id, nombre, pais, sitio_web)
        )
        print("\nEditorial actualizada.")

    @manejar_errores
    def _baja_editorial(self) -> None:
        editorial = self._s.editoriales.buscar(
            pedir_entero("Id de la editorial a eliminar")
        )
        if confirmar(f"¿Eliminar la editorial '{editorial.nombre}'?"):
            self._s.editoriales.eliminar(editorial.id)
            print("\nEditorial eliminada.")

    def _menu_monedas(self) -> None:
        self._menu_crud(
            "Monedas",
            self._listar_monedas,
            self._alta_moneda,
            self._modificar_moneda,
            self._baja_moneda,
        )

    @manejar_errores
    def _listar_monedas(self) -> None:
        mostrar_tabla(
            ["Id", "Código", "Nombre", "Símbolo"],
            [
                [m.id, m.codigo, m.nombre, m.simbolo]
                for m in self._s.monedas.listar()
            ],
        )

    @manejar_errores
    def _alta_moneda(self) -> None:
        print("\nNueva moneda")
        codigo = pedir_texto("Código (3 letras)")
        nombre = pedir_texto("Nombre")
        simbolo = pedir_texto("Símbolo")
        moneda = self._s.monedas.crear(Moneda(0, codigo, nombre, simbolo))
        print(f"\nMoneda creada con id {moneda.id}.")

    @manejar_errores
    def _modificar_moneda(self) -> None:
        moneda = self._s.monedas.buscar(
            pedir_entero("Id de la moneda a modificar")
        )
        print("Enter para mantener el valor actual.")
        codigo = pedir_texto("Código (3 letras)", moneda.codigo)
        nombre = pedir_texto("Nombre", moneda.nombre)
        simbolo = pedir_texto("Símbolo", moneda.simbolo)
        self._s.monedas.actualizar(Moneda(moneda.id, codigo, nombre, simbolo))
        print("\nMoneda actualizada.")

    @manejar_errores
    def _baja_moneda(self) -> None:
        moneda = self._s.monedas.buscar(
            pedir_entero("Id de la moneda a eliminar")
        )
        if confirmar(f"¿Eliminar la moneda {moneda}?"):
            self._s.monedas.eliminar(moneda.id)
            print("\nMoneda eliminada.")

    def _menu_precios(self) -> None:
        self._menu_crud(
            "Precios",
            self._listar_precios,
            self._alta_precio,
            self._modificar_precio,
            self._baja_precio,
        )

    @manejar_errores
    def _listar_precios(self) -> None:
        mostrar_tabla(
            ["Id", "Libro", "Moneda", "Monto"],
            [
                [p.id, p.libro.titulo, p.moneda.codigo, p]
                for p in self._s.precios.listar()
            ],
        )

    @manejar_errores
    def _alta_precio(self) -> None:
        print("\nNuevo precio")
        libro = self._s.libros.buscar(pedir_entero("Id del libro"))
        moneda = self._elegir(self._s.monedas, "Moneda")
        monto = pedir_decimal("Monto")
        precio = self._s.precios.crear(Precio(0, libro, moneda, monto))
        print(f"\nPrecio creado con id {precio.id}.")

    @manejar_errores
    def _modificar_precio(self) -> None:
        precio = self._s.precios.buscar(
            pedir_entero("Id del precio a modificar")
        )
        print(f"Libro: {precio.libro}")
        moneda = self._elegir(self._s.monedas, "Moneda", precio.moneda)
        monto = pedir_decimal("Monto", precio.monto)
        self._s.precios.actualizar(
            Precio(precio.id, precio.libro, moneda, monto)
        )
        print("\nPrecio actualizado.")

    @manejar_errores
    def _baja_precio(self) -> None:
        precio = self._s.precios.buscar(
            pedir_entero("Id del precio a eliminar")
        )
        if confirmar(
            f"¿Eliminar el precio {precio} de '{precio.libro.titulo}'?"
        ):
            self._s.precios.eliminar(precio.id)
            print("\nPrecio eliminado.")

    def _menu_stock(self) -> None:
        self._menu_crud(
            "Stock",
            self._listar_stock,
            self._alta_stock,
            self._modificar_stock,
            self._baja_stock,
            [
                ("Reponer unidades", self._reponer_stock),
                ("Descontar unidades", self._descontar_stock),
            ],
        )

    @staticmethod
    def _tabla_stock(registros: list) -> None:
        mostrar_tabla(
            ["Libro", "Título", "Cantidad", "Mínimo"],
            [
                [s.libro_id, s.libro.titulo, s.cantidad, s.cantidad_minima]
                for s in registros
            ],
        )

    @manejar_errores
    def _listar_stock(self) -> None:
        self._tabla_stock(self._s.stock.listar())

    @manejar_errores
    def _alta_stock(self) -> None:
        libro_id = pedir_entero("Id del libro")
        cantidad = pedir_entero("Cantidad")
        minima = pedir_entero("Cantidad mínima", 5)
        self._s.stock.crear(libro_id, cantidad, minima)
        print("\nStock cargado.")

    @manejar_errores
    def _modificar_stock(self) -> None:
        stock = self._s.stock.buscar(pedir_entero("Id del libro"))
        print(f"Libro: {stock.libro}")
        cantidad = pedir_entero("Cantidad", stock.cantidad)
        minima = pedir_entero("Cantidad mínima", stock.cantidad_minima)
        self._s.stock.actualizar(stock.libro_id, cantidad, minima)
        print("\nStock actualizado.")

    @manejar_errores
    def _baja_stock(self) -> None:
        stock = self._s.stock.buscar(pedir_entero("Id del libro"))
        if confirmar(f"¿Eliminar el stock de '{stock.libro.titulo}'?"):
            self._s.stock.eliminar(stock.libro_id)
            print("\nStock eliminado.")

    @manejar_errores
    def _reponer_stock(self) -> None:
        libro_id = pedir_entero("Id del libro")
        cantidad = pedir_entero("Unidades que ingresan")
        stock = self._s.stock.reponer(libro_id, cantidad)
        print(f"\nStock actualizado: {stock}")

    @manejar_errores
    def _descontar_stock(self) -> None:
        libro_id = pedir_entero("Id del libro")
        cantidad = pedir_entero("Unidades que salen")
        stock = self._s.stock.descontar(libro_id, cantidad)
        print(f"\nStock actualizado: {stock}")

    def _menu_tipos_cotizacion(self) -> None:
        self._menu_crud(
            "Tipos de cotización",
            self._listar_tipos,
            self._alta_tipo,
            self._modificar_tipo,
            self._baja_tipo,
        )

    @manejar_errores
    def _listar_tipos(self) -> None:
        mostrar_tabla(
            ["Id", "Código", "Nombre"],
            [
                [t.id, t.codigo, t.nombre]
                for t in self._s.tipos_cotizacion.listar()
            ],
        )

    @manejar_errores
    def _alta_tipo(self) -> None:
        print("\nNuevo tipo de cotización")
        print(
            "El código tiene que coincidir con el de DolarApi para que se "
            "actualice solo."
        )
        codigo = pedir_texto("Código")
        nombre = pedir_texto("Nombre")
        tipo = self._s.tipos_cotizacion.crear(
            TipoCotizacion(0, codigo, nombre)
        )
        print(f"\nTipo de cotización creado con id {tipo.id}.")

    @manejar_errores
    def _modificar_tipo(self) -> None:
        tipo = self._s.tipos_cotizacion.buscar(
            pedir_entero("Id del tipo a modificar")
        )
        print("Enter para mantener el valor actual.")
        codigo = pedir_texto("Código", tipo.codigo)
        nombre = pedir_texto("Nombre", tipo.nombre)
        self._s.tipos_cotizacion.actualizar(
            TipoCotizacion(tipo.id, codigo, nombre)
        )
        print("\nTipo de cotización actualizado.")

    @manejar_errores
    def _baja_tipo(self) -> None:
        tipo = self._s.tipos_cotizacion.buscar(
            pedir_entero("Id del tipo a eliminar")
        )
        if confirmar(f"¿Eliminar el tipo {tipo}?"):
            self._s.tipos_cotizacion.eliminar(tipo.id)
            print("\nTipo de cotización eliminado.")

    def _menu_cotizaciones(self) -> None:
        self._menu_crud(
            "Cotizaciones del dólar",
            self._listar_cotizaciones,
            self._alta_cotizacion,
            self._modificar_cotizacion,
            self._baja_cotizacion,
            [("Actualizar desde DolarApi", self._actualizar_cotizaciones)],
        )

    @staticmethod
    def _tabla_cotizaciones(cotizaciones: list) -> None:
        mostrar_tabla(
            ["Tipo", "Fecha", "Compra", "Venta"],
            [
                [
                    c.tipo.nombre,
                    c.fecha,
                    formato_pesos(c.compra),
                    formato_pesos(c.venta),
                ]
                for c in cotizaciones
            ],
        )

    @manejar_errores
    def _listar_cotizaciones(self) -> None:
        self._tabla_cotizaciones(self._s.cotizaciones.listar())

    @manejar_errores
    def _alta_cotizacion(self) -> None:
        tipo = self._elegir(self._s.tipos_cotizacion, "Tipo")
        fecha = pedir_fecha("Fecha")
        compra = pedir_decimal("Valor de compra")
        venta = pedir_decimal("Valor de venta")
        self._s.cotizaciones.crear(tipo.id, fecha, compra, venta)
        print("\nCotización cargada.")

    @manejar_errores
    def _modificar_cotizacion(self) -> None:
        tipo = self._elegir(self._s.tipos_cotizacion, "Tipo")
        fecha = pedir_fecha("Fecha")
        cotizacion = self._s.cotizaciones.buscar(tipo.id, fecha)
        compra = pedir_decimal("Valor de compra", cotizacion.compra)
        venta = pedir_decimal("Valor de venta", cotizacion.venta)
        self._s.cotizaciones.actualizar(tipo.id, fecha, compra, venta)
        print("\nCotización actualizada.")

    @manejar_errores
    def _baja_cotizacion(self) -> None:
        tipo = self._elegir(self._s.tipos_cotizacion, "Tipo")
        fecha = pedir_fecha("Fecha")
        cotizacion = self._s.cotizaciones.buscar(tipo.id, fecha)
        if confirmar(f"¿Eliminar la cotización {cotizacion}?"):
            self._s.cotizaciones.eliminar(tipo.id, fecha)
            print("\nCotización eliminada.")

    def _actualizar_cotizaciones(self) -> None:
        print("\nConsultando cotizaciones en DolarApi...")
        try:
            cantidad = self._s.cotizaciones.actualizar_desde_api()
            print(f"Se actualizaron {cantidad} cotizaciones del día.")
        except ConnectionError as error:
            print(f"{error}\nSe usan las últimas cotizaciones guardadas.")

    def _menu_reportes(self) -> None:
        while True:
            print("\n--- Reportes ---")
            print("1. Cotizar un libro con todos los tipos de dólar")
            print("2. Catálogo con precios en pesos")
            print("3. Libros con stock bajo")
            print("4. Histórico de cotizaciones de un tipo")
            print("0. Volver")
            opcion = input("Opción: ").strip()

            match opcion:
                case "1":
                    self._reporte_cotizar_libro()
                case "2":
                    self._reporte_catalogo()
                case "3":
                    self._reporte_stock_bajo()
                case "4":
                    self._reporte_historico()
                case "0":
                    return
                case _:
                    print("Opción inválida.")

    @manejar_errores
    def _reporte_cotizar_libro(self) -> None:
        libro = self._s.libros.buscar(pedir_entero("Id del libro"))
        print(f"\n{libro}")
        for precio in self._s.precios.precios_de_libro(libro.id):
            print(f"Precio cargado: {precio}")
        mostrar_tabla(
            [
                "Cotización",
                "Fecha",
                "Venta",
                "Precio en pesos",
                "Precio en dólares",
            ],
            [
                [
                    c.tipo.nombre,
                    c.fecha,
                    formato_pesos(c.venta),
                    formato_pesos(pesos),
                    f"US$ {dolares:,.2f}",
                ]
                for c, pesos, dolares in self._s.cotizador.cotizar_libro(
                    libro.id
                )
            ],
        )

    @manejar_errores
    def _reporte_catalogo(self) -> None:
        tipo = self._elegir(self._s.tipos_cotizacion, "Tipo")
        ultima = self._s.cotizaciones.ultima(tipo.id)
        if ultima is None:
            print(f"\nNo hay cotizaciones cargadas del tipo {tipo}.")
            return
        print(f"\nSe usa la cotización {ultima}")
        mostrar_tabla(
            ["Id", "Título", "Autor", "Precio en pesos"],
            [
                [libro.id, libro.titulo, libro.autor, formato_pesos(pesos)]
                for libro, pesos in self._s.reportes.catalogo_en_pesos(tipo.id)
            ],
        )

    @manejar_errores
    def _reporte_stock_bajo(self) -> None:
        self._tabla_stock(self._s.reportes.stock_bajo())

    @manejar_errores
    def _reporte_historico(self) -> None:
        tipo = self._elegir(self._s.tipos_cotizacion, "Tipo")
        self._tabla_cotizaciones(self._s.cotizaciones.historico(tipo.id))
