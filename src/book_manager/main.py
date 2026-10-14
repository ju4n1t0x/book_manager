
"""Punto de entrada del sistema Book Manager."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from book_manager.database.connection import ConexionDB
from book_manager.preload_data.preload_data import cargar_datos_iniciales
from book_manager.repositories.repositories import Repositorios
from book_manager.services import DolarApi, Servicios
from book_manager.ui.console import Consola


def main(import_default_data: bool = False) -> None:
    """Arma el sistema y abre el menú de consola."""

    if import_default_data:
        for archivo, cantidad in cargar_datos_iniciales().items():
            print(f"Cargados {cantidad} registros en {archivo}.csv")

    ruta_env = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(dotenv_path=ruta_env)

    url = os.getenv("DIRECT_URL")

    if not url:
        raise ValueError(
            "La variable DIRECT_URL no está definida en el .env."
        )

    conexion = ConexionDB(url)

    try:
        repositorios = Repositorios(conexion)
        servicios = Servicios(repositorios, DolarApi())
        Consola(servicios).iniciar()
    finally:
        conexion.close()


if __name__ == "__main__":
    main(import_default_data="--importar" in sys.argv)
