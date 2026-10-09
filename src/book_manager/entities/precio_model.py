
from book_manager.entities.entidad_base_model import EntidadBase, _validar_positivo
from book_manager.entities.libro_model import Libro
from book_manager.entities.moneda_model import Moneda

class Precio(EntidadBase):
    """Precio de un libro expresado en una moneda."""

    def __init__(
        self, id: int, libro: Libro, moneda: Moneda, monto: float
    ) -> None:
        super().__init__(id)
        self.libro = libro
        self.moneda = moneda
        self.monto = monto

    @property
    def libro(self) -> Libro:
        return self._libro

    @libro.setter
    def libro(self, valor: Libro) -> None:
        if not isinstance(valor, Libro):
            raise ValueError("El precio debe estar asociado a un libro.")
        self._libro = valor

    @property
    def moneda(self) -> Moneda:
        return self._moneda

    @moneda.setter
    def moneda(self, valor: Moneda) -> None:
        if not isinstance(valor, Moneda):
            raise ValueError("El precio debe tener una moneda válida.")
        self._moneda = valor

    @property
    def monto(self) -> float:
        return self._monto

    @monto.setter
    def monto(self, valor: float) -> None:
        self._monto = round(_validar_positivo(valor, "monto"), 2)

    def __str__(self) -> str:
        return f"{self.moneda.simbolo} {self.monto:,.2f}"