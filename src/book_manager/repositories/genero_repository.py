
from book_manager.entities import Genero
from book_manager.repositories.archivo_csv_repository import RepositorioCSV

class RepositorioGenero(RepositorioCSV[Genero]):
    """Repositorio de géneros."""

    campos = ["id", "nombre", "descripcion"]

    def _a_fila(self, entidad: Genero) -> dict:
        return {
            "id": entidad.id,
            "nombre": entidad.nombre,
            "descripcion": entidad.descripcion,
        }

    def _desde_fila(self, fila: dict[str, str]) -> Genero:
        return Genero(int(fila["id"]), fila["nombre"], fila["descripcion"])