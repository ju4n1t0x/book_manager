
from book_manager.entities import Editorial
from book_manager.repositories.archivo_csv_repository import RepositorioCSV

class RepositorioEditorial(RepositorioCSV[Editorial]):
    """Repositorio de editoriales."""

    campos = ["id", "nombre", "pais", "sitio_web"]

    def _a_fila(self, entidad: Editorial) -> dict:
        return {
            "id": entidad.id,
            "nombre": entidad.nombre,
            "pais": entidad.pais,
            "sitio_web": entidad.sitio_web,
        }

    def _desde_fila(self, fila: dict[str, str]) -> Editorial:
        return Editorial(
            int(fila["id"]), fila["nombre"], fila["pais"], fila["sitio_web"]
        )
