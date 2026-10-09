
from book_manager.entities import TipoCotizacion
from book_manager.repositories.archivo_csv_repository import RepositorioCSV


class RepositorioTipoCotizacion(RepositorioCSV[TipoCotizacion]):
    """Repositorio de tipos de cotización."""

    campos = ["id", "codigo", "nombre"]

    def _a_fila(self, entidad: TipoCotizacion) -> dict:
        return {
            "id": entidad.id,
            "codigo": entidad.codigo,
            "nombre": entidad.nombre,
        }

    def _desde_fila(self, fila: dict[str, str]) -> TipoCotizacion:
        return TipoCotizacion(int(fila["id"]), fila["codigo"], fila["nombre"])