import datetime
from book_manager.entities.entidad_base_model import EntidadBase, _validar_texto
from book_manager.entities.editorial_model import Editorial
from book_manager.entities.genero_model import Genero

class Libro(EntidadBase):
    """Título del catálogo de la librería."""

    def __init__(
        self,
        id: int,
        isbn: str,
        titulo: str,
        autor: str,
        editorial: Editorial,
        genero: Genero,
        anio_publicacion: int,
    ) -> None:
        super().__init__(id)
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.editorial = editorial
        self.genero = genero
        self.anio_publicacion = anio_publicacion

    @property
    def isbn(self) -> str:
        return self._isbn

    @isbn.setter
    def isbn(self, valor: str) -> None:
        valor = _validar_texto(valor, "ISBN").replace("-", "").replace(" ", "")
        if not valor.isdigit() or len(valor) not in (10, 13):
            raise ValueError("El ISBN debe tener 10 o 13 dígitos.")
        self._isbn = valor

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        self._titulo = _validar_texto(valor, "título")

    @property
    def autor(self) -> str:
        return self._autor

    @autor.setter
    def autor(self, valor: str) -> None:
        self._autor = _validar_texto(valor, "autor")

    @property
    def editorial(self) -> Editorial:
        return self._editorial

    @editorial.setter
    def editorial(self, valor: Editorial) -> None:
        if not isinstance(valor, Editorial):
            raise ValueError("El libro debe tener una editorial válida.")
        self._editorial = valor

    @property
    def genero(self) -> Genero:
        return self._genero

    @genero.setter
    def genero(self, valor: Genero) -> None:
        if not isinstance(valor, Genero):
            raise ValueError("El libro debe tener un género válido.")
        self._genero = valor

    @property
    def anio_publicacion(self) -> int:
        return self._anio_publicacion

    @anio_publicacion.setter
    def anio_publicacion(self, valor: int) -> None:
        valor = int(valor)
        if valor < 1450 or valor > datetime.date.today().year:
            raise ValueError("El año de publicación no es válido.")
        self._anio_publicacion = valor

    def __str__(self) -> str:
        return f"{self.titulo} - {self.autor}"