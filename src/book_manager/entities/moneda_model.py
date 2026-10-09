
from book_manager.entities.entidad_base_model import EntidadBase, _validar_texto

class Moneda(EntidadBase):
    """Moneda en la que se puede expresar un precio.

    El código usa el formato ISO 4217: tres letras (ARS, USD, EUR).
    """

    def __init__(
        self, id: int, codigo: str, nombre: str, simbolo: str
    ) -> None:
        super().__init__(id)
        self.codigo = codigo
        self.nombre = nombre
        self.simbolo = simbolo

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        valor = _validar_texto(valor, "código").upper()
        if len(valor) != 3 or not valor.isalpha():
            raise ValueError(
                "El código de moneda debe tener 3 letras, por ejemplo ARS."
            )
        self._codigo = valor

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = _validar_texto(valor, "nombre")

    @property
    def simbolo(self) -> str:
        return self._simbolo

    @simbolo.setter
    def simbolo(self, valor: str) -> None:
        self._simbolo = _validar_texto(valor, "símbolo")

    def __str__(self) -> str:
        return f"{self.codigo} ({self.simbolo})"