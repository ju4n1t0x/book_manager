
from book_manager.entities.entidad_base_model import EntidadBase, _validar_texto

class Genero(EntidadBase):
    """Categoría literaria a la que pertenece un libro."""

    def __init__(self, id: int, nombre: str, descripcion: str = "") -> None:
        super().__init__(id)
        self.nombre = nombre
        self.descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = _validar_texto(valor, "nombre")

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        self._descripcion = str(valor).strip()

    def __str__(self) -> str:
        return self.nombre