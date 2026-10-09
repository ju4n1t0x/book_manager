
from book_manager.repositories.archivo_csv_repository import RepositorioCSV
from book_manager.entities import Moneda


class RepositorioMoneda(RepositorioCSV[Moneda]):
    """Repositorio de monedas."""

    campos = ["id", "codigo", "nombre", "simbolo"]

    def _a_fila(self, entidad: Moneda) -> dict:
        return {
            "id": entidad.id,
            "codigo": entidad.codigo,
            "nombre": entidad.nombre,
            "simbolo": entidad.simbolo,
        }

    def _desde_fila(self, fila: dict[str, str]) -> Moneda:
        return Moneda(
            int(fila["id"]), fila["codigo"], fila["nombre"], fila["simbolo"]
        )
