
from book_manager.entities.entidad_base_model import EntidadBase, _validar_texto


class TipoCotizacion(EntidadBase):
    """Tipo de cotización del dólar (Oficial, Blue, MEP, etc.).

    El código coincide con el que usa DolarApi para identificar cada
    cotización.
    """

    def __init__(self, id: int, codigo: str, nombre: str) -> None:
        super().__init__(id)
        self.codigo = codigo
        self.nombre = nombre

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        self._codigo = _validar_texto(valor, "código").lower()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = _validar_texto(valor, "nombre")

    def __str__(self) -> str:
        return self.nombre