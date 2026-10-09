"""Punto de entrada del sistema Book Manager."""

import sys

from book_manager.preload_data.preload_data import cargar_datos_iniciales
from book_manager.repositories.repositories import Repositorios
from book_manager.services import DolarApi, Servicios
from book_manager.ui.console import Consola


def main(import_default_data: bool = False) -> None:
    """Arma el sistema y abre el menú de consola.

    Args:
        import_default_data (bool): Si es True, antes de empezar se
            escriben los datos iniciales en migrations/csv (se pierden los
            datos actuales).
    """
    if import_default_data:
        for archivo, cantidad in cargar_datos_iniciales().items():
            print(f"Cargados {cantidad} registros en {archivo}.csv")

    repositorios = Repositorios()
    servicios = Servicios(repositorios, DolarApi())
    Consola(servicios).iniciar()


if __name__ == "__main__":
    main(import_default_data="--importar" in sys.argv)
