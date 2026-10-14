
from book_manager.entities.entidad_base_model import _validar_positivo
from book_manager.entities.libro_model import Libro

class Stock:
    """Cantidad disponible de un libro. Se identifica por el libro."""

    def __init__(
        self, libro: Libro, cantidad: int, cantidad_minima: int = 5
    ) -> None:
        self.libro = libro
        self.cantidad = cantidad
        self.cantidad_minima = cantidad_minima

    @property
    def libro(self) -> Libro:
        return self._libro

    @libro.setter
    def libro(self, valor: Libro) -> None:
        if not isinstance(valor, Libro):
            raise ValueError("El stock debe estar asociado a un libro.")
        self._libro = valor

    @property
    def libro_id(self) -> int:
        return self._libro.id

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        valor = int(valor)
        if valor < 0:
            raise ValueError("La cantidad en stock no puede ser negativa.")
        self._cantidad = valor

    @property
    def cantidad_minima(self) -> int:
        return self._cantidad_minima

    @cantidad_minima.setter
    def cantidad_minima(self, valor: int) -> None:
        valor = int(valor)
        if valor < 0:
            raise ValueError("La cantidad mínima no puede ser negativa.")
        self._cantidad_minima = valor

    def __str__(self) -> str:
        return f"{self.libro.titulo}: {self.cantidad} unidades"
