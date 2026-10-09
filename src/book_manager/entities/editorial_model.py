
from book_manager.entities.entidad_base_model import EntidadBase, _validar_texto


class Editorial(EntidadBase):
    """Proveedor o distribuidora que le vende los libros a la librería."""

    def __init__(
        self, id: int, nombre: str, pais: str, sitio_web: str = ""
    ) -> None:
        super().__init__(id)
        self.nombre = nombre
        self.pais = pais
        self.sitio_web = sitio_web

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = _validar_texto(valor, "nombre")

    @property
    def pais(self) -> str:
        return self._pais

    @pais.setter
    def pais(self, valor: str) -> None:
        self._pais = _validar_texto(valor, "país")

    @property
    def sitio_web(self) -> str:
        return self._sitio_web

    @sitio_web.setter
    def sitio_web(self, valor: str) -> None:
        self._sitio_web = str(valor).strip()

    def __str__(self) -> str:
        return self.nombre