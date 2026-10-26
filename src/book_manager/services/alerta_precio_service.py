"""Alertas por diferencia entre el precio interno y el precio web."""

import csv
import datetime
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from book_manager.entities import Libro
from book_manager.services.cotizacion_service import CotizadorService
from book_manager.services.libro_service import LibroService


@dataclass(frozen=True)
class Alerta:
    """Diferencia de precio detectada entre el catálogo y la web."""

    fecha_extraccion: str
    libro_id: int
    isbn: str
    titulo: str
    autor: str
    precio_interno: float
    precio_web: float
    diferencia: float
    diferencia_porcentual: float
    situacion: str
    url: str


class AlertaPrecioService:
    """Compara el precio interno de los libros con el precio de la web.

    La diferencia se calcula como precio web menos precio interno, ambos en
    pesos. Se genera una alerta cuando su valor absoluto alcanza el mínimo
    indicado por el usuario.
    """

    def __init__(
        self, libros: LibroService, cotizador: CotizadorService
    ) -> None:
        self._libros = libros
        self._cotizador = cotizador

    @staticmethod
    def _clave(titulo: str, autor: str) -> Tuple[str, str]:
        """Clave para relacionar un resultado del scraper con un libro."""
        return titulo.strip().casefold(), autor.strip().casefold()

    @staticmethod
    def leer_resultados(ruta: Path) -> List[Dict[str, str]]:
        """Lee el csv que genera el scraper.

        Args:
            ruta (Path): Archivo csv con los resultados del scraper.

        Returns:
            List[Dict[str, str]]: Una fila por resultado encontrado en la web.

        Raises:
            FileNotFoundError: Si el archivo no existe.
        """
        if not ruta.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo de resultados: {ruta}"
            )
        with open(ruta, encoding="utf-8-sig", newline="") as archivo:
            return list(csv.DictReader(archivo))

    def comparar(
        self,
        resultados: List[Dict[str, str]],
        diferencia_minima: float,
        tipo_cotizacion_id: int,
    ) -> List[Alerta]:
        """Compara los resultados del scraper con los precios internos.

        Los libros con precio en dólares se pasan a pesos con la última
        cotización del tipo indicado. Los libros sin precio interno, o con
        un precio web inválido, se ignoran.

        Args:
            resultados (List[Dict[str, str]]): Filas del csv del scraper.
            diferencia_minima (float): Diferencia absoluta, en pesos, a
                partir de la cual se genera la alerta.
            tipo_cotizacion_id (int): Tipo de dólar usado para convertir.

        Returns:
            List[Alerta]: Alertas ordenadas de mayor a menor diferencia.

        Raises:
            ValueError: Si la diferencia mínima es negativa.
        """
        if diferencia_minima < 0:
            raise ValueError("La diferencia mínima no puede ser negativa.")

        catalogo: Dict[Tuple[str, str], Libro] = {}
        for libro in self._libros.listar():
            catalogo.setdefault(self._clave(libro.titulo, libro.autor), libro)

        precios_internos: Dict[int, Optional[float]] = {}
        fecha = datetime.date.today().isoformat()
        alertas: List[Alerta] = []

        for fila in resultados:
            libro = catalogo.get(
                self._clave(
                    fila.get("titulo_buscado", ""),
                    fila.get("autor_buscado", ""),
                )
            )
            if libro is None:
                continue

            if libro.id not in precios_internos:
                precios_internos[libro.id] = self._cotizador.precio_en_pesos(
                    libro.id, tipo_cotizacion_id
                )
            interno = precios_internos[libro.id]
            if not interno:
                continue

            try:
                web = float(fila["precio"])
            except (KeyError, ValueError):
                continue

            diferencia = round(web - interno, 2)
            if diferencia == 0 or abs(diferencia) < diferencia_minima:
                continue

            alertas.append(
                Alerta(
                    fecha_extraccion=fecha,
                    libro_id=libro.id,
                    isbn=libro.isbn,
                    titulo=libro.titulo,
                    autor=libro.autor,
                    precio_interno=interno,
                    precio_web=web,
                    diferencia=diferencia,
                    diferencia_porcentual=round(diferencia / interno * 100, 2),
                    situacion=(
                        "Competidor más barato"
                        if diferencia < 0
                        else "Competidor más caro"
                    ),
                    url=fila.get("url", ""),
                )
            )

        return sorted(alertas, key=lambda a: abs(a.diferencia), reverse=True)

    @staticmethod
    def guardar(alertas: List[Alerta], carpeta: Path) -> Path:
        """Guarda las alertas en un csv nuevo dentro de la carpeta.

        El nombre incluye fecha y hora, así cada ejecución genera su propio
        archivo. Se crea aunque no haya alertas.

        Args:
            alertas (List[Alerta]): Alertas a guardar.
            carpeta (Path): Carpeta de destino.

        Returns:
            Path: Ruta del archivo generado.
        """
        carpeta.mkdir(parents=True, exist_ok=True)
        marca = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = carpeta / f"alertas_precios_{marca}.csv"
        columnas = [campo.name for campo in fields(Alerta)]
        with open(ruta, "w", encoding="utf-8-sig", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=columnas)
            escritor.writeheader()
            for alerta in alertas:
                escritor.writerow(asdict(alerta))
        return ruta

    def generar(
        self,
        ruta_resultados: Path,
        carpeta_alertas: Path,
        diferencia_minima: float,
        tipo_cotizacion_id: int,
    ) -> Tuple[Path, int]:
        """Lee los resultados del scraper y genera el csv de alertas.

        Args:
            ruta_resultados (Path): Csv que dejó el scraper.
            carpeta_alertas (Path): Carpeta donde se guarda el csv de alertas.
            diferencia_minima (float): Diferencia mínima, en pesos, ingresada
                por el usuario.
            tipo_cotizacion_id (int): Tipo de dólar usado para convertir.

        Returns:
            Tuple[Path, int]: Ruta del archivo generado y cantidad de alertas.
        """
        resultados = self.leer_resultados(ruta_resultados)
        alertas = self.comparar(
            resultados, diferencia_minima, tipo_cotizacion_id
        )
        return self.guardar(alertas, carpeta_alertas), len(alertas)