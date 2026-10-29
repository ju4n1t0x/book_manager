
"""Punto de entrada del sistema Book Manager."""
import os
import sys
from pathlib import Path
from book_manager.repositories.repositories import Repositorios
from book_manager.services import DolarApi, Servicios
from book_manager.ui.console import Consola
from book_manager.database.connection import ConexionDB
from dotenv import load_dotenv
from book_manager.models.models import crear_tablas


RUTA_ENV = Path(__file__).resolve().parent / ".env"
RUTA_MIGRACIONES = Path(__file__).resolve().parent / "migrations"

def main(import_default_data: bool = False) -> None:
    """Arma el sistema y abre el menú de consola."""

   

    load_dotenv(RUTA_ENV)

    if import_default_data:
        from book_manager.migrations.migrations import migrar_datos
        from book_manager.preload_data.preload_data import cargar_datos_iniciales
        for archivo, cantidad in cargar_datos_iniciales().items():
            print(f"Cargados {cantidad} registros en {archivo}.csv")

        migrar_datos(
            str(RUTA_MIGRACIONES / "csv"),
            str(RUTA_MIGRACIONES / "sql")
        )
    
    url= os.getenv("DIRECT_URL")

    if not url:
        raise ValueError(f"La variable de entorno 'DIRECT_URL' "
                         f"no está definida en el archivo .env.")

    conexion = ConexionDB(url)
    
    try:
        conexion.connect()
        crear_tablas(conexion.engine)
        repositorios = Repositorios(conexion)
        servicios = Servicios(repositorios, DolarApi())
        Consola(servicios).iniciar()
    finally:
        conexion.close()
        
    


if __name__ == "__main__":
    main(import_default_data="--importar" in sys.argv)
