"""Punto de entrada del sistema Book Manager."""

from pathlib import Path
import sys


src_path = Path(__file__).resolve().parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from book_manager.preload_data.preload_data import importar_datos
from book_manager.repositories.repositories import Repositorios
from book_manager.services.services import DolarApi, Servicios
from book_manager.ui.console import Consola


def main(import_default_data: bool = False) -> None:
    """Arma el sistema y abre el menú de consola.

    Args:
        import_default_data (bool): Si es True, antes de empezar se cargan los
            datos iniciales de migrations/csv (se pierden los datos actuales).
    """
    repositorios = Repositorios()
    if import_default_data:
        for archivo, cantidad in importar_datos(repositorios).items():
            print(f"Importados {cantidad} registros de {archivo}.csv")

    servicios = Servicios(repositorios, DolarApi())
    Consola(servicios).iniciar()


if __name__ == "__main__":
    main(import_default_data="--importar" in sys.argv)