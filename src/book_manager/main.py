"""Punto de entrada del sistema Book Manager."""
import os
import sys
from pathlib import Path
from book_manager.repositories.repositories import Repositorios
from book_manager.services import DolarApi, Servicios
from book_manager.ui.console import Consola
from book_manager.database.connection import ConexionDB
from dotenv import load_dotenv


def main(import_default_data: bool = False) -> None:
    """Arma el sistema y abre el menú de consola.

    Args:
        import_default_data (bool): Si es True, antes de empezar se
            escriben los datos iniciales en migrations/csv (se pierden los
            datos actuales).
    """

    load_dotenv(Path("src/book_manager/.env"))

    if import_default_data:
        from book_manager.preload_data.preload_data import cargar_datos_iniciales
        for archivo, cantidad in cargar_datos_iniciales().items():
            print(f"Cargados {cantidad} registros en {archivo}.csv")

  
    
    url = os.getenv("DIRECT_URL")

    if not url:
        raise ValueError("La variable de entorno 'DIRECT_URL' no está definida en el archivo .env.")

    conexion = ConexionDB(url)
    repositorios = Repositorios(conexion)
    servicios = Servicios(repositorios, DolarApi())
    try:
        Consola(servicios).iniciar()
    finally:
        conexion.close()
        
    


if __name__ == "__main__":
    main(import_default_data="--importar" in sys.argv)
