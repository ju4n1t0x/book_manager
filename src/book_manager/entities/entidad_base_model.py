"""Entidades del sistema de gestión de la librería."""

import abc


def _validar_texto(valor: str, campo: str) -> str:
    """Valida que un texto no esté vacío y lo devuelve sin espacios extra.

    Args:
        valor (str): Texto a validar.
        campo (str): Nombre del campo, se usa en el mensaje de error.

    Returns:
        str: El texto sin espacios al principio ni al final.
    """
    valor = str(valor).strip()
    if not valor:
        raise ValueError(f"El campo {campo} es obligatorio.")
    return valor


def _validar_positivo(valor: float, campo: str) -> float:
    """Valida que un número sea mayor a cero."""
    valor = float(valor)
    if valor <= 0:
        raise ValueError(f"El campo {campo} debe ser mayor a cero.")
    return valor


class EntidadBase(abc.ABC):
    """Clase base de las entidades que se identifican por un id.

    El id 0 indica que la entidad todavía no fue guardada; el repositorio
    le asigna uno nuevo al crearla.
    """

    def __init__(self, id: int = 0) -> None:
        self.id = id

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, valor: int) -> None:
        valor = int(valor)
        if valor < 0:
            raise ValueError("El id no puede ser negativo.")
        self._id = valor

    def __eq__(self, otro: object) -> bool:
        return type(self) is type(otro) and self.id == otro.id

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.id))
























