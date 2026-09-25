"""Importación de los datos iniciales desde la carpeta migrations/csv."""

from pathlib import Path

from book_manager.repositories.repositories import Repositorios

DIRECTORIO_MIGRACIONES = Path(__file__).resolve().parent.parent / "migrations" / "csv"


def importar_datos(
    repositorios: Repositorios, directorio: Path = DIRECTORIO_MIGRACIONES
) -> dict[str, int]:
    """Carga en los repositorios los datos de los archivos de migración.

    Los datos que había se reemplazan. Cada archivo se llama igual que su
    repositorio, por ejemplo generos.csv.

    Args:
        repositorios (Repositorios): Repositorios donde se cargan los datos.
        directorio (Path): Carpeta con los archivos CSV.

    Returns:
        dict[str, int]: Cantidad de registros importados por archivo.
    """
    importados = {}
    for nombre, repositorio in repositorios.en_orden():
        ruta = directorio / f"{nombre}.csv"
        if not ruta.exists():
            raise FileNotFoundError(f"Falta el archivo de migración {ruta.name}.")
        importados[nombre] = repositorio.importar_desde(ruta)
    return importados
