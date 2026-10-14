from abc import abstractmethod
from typing import Generic, List, Optional, TypeVar, Type

from sqlalchemy import select
from sqlalchemy.orm import Session

from book_manager.database.connection import ConexionDB
from book_manager.entities import EntidadBase
from book_manager.models.models import Base
from book_manager.repositories.irepositorio import IRepositorio

Entidad = TypeVar("Entidad", bound=EntidadBase)
Modelo = TypeVar("Modelo", bound=Base)

class RepositorioSqlAlchemy(IRepositorio[Entidad], Generic[Entidad, Modelo]):
    """Repositorio base para entidades que se almacenan en una base de datos SQL mediante SQLAlchemy.

    Las clases concretas heredan el CRUD y definen:
    - La conversión entre modelo y entidad.
    - La creación del modelo ORM.
    - La actualización del modelo ORM.

    """

    modelo: Type[Modelo]

    def __init__(self, conexion: ConexionDB) -> None:
        self._conexion = conexion

    @abstractmethod
    def _a_entidad(self, modelo: Modelo) -> Entidad:
        """Convierte un modelo de SQLAlchemy en una entidad del dominio."""
        

    @abstractmethod
    def _crear_modelo(
        self,
        sesion: Session,
        entidad: Entidad,
        ) -> Modelo:
        """Crea un modelo de SQLAlchemy a partir de una entidad del dominio."""
        

    @abstractmethod
    def _actualizar_modelo(
        self,
        sesion: Session,
        modelo: Modelo,
        entidad: Entidad
    ) -> None:
        """Actualiza un modelo de SQLAlchemy a partir de una entidad del dominio."""
        

    def crear(self, entidad: Entidad) -> Entidad:
        """ Alta de una entidad ."""
        with self._conexion.transaccion() as sesion:
            modelo = self._crear_modelo(
                sesion, 
                entidad
            )

            entidad_id = getattr(entidad, "id", 0)
            if entidad_id != 0:
                setattr(modelo, "id", entidad_id)

            

            sesion.add(modelo)
            sesion.flush()  

            setattr(entidad, "id", getattr(modelo, "id"))

            return self._a_entidad(modelo)

    def leer_por_id(
            self,
            id: int
    ) -> Optional[Entidad]:
        """Lee una entidad por su ID."""

        with self._conexion.transaccion() as sesion:
            modelo = sesion.get(
                self.modelo,
                id
            )

            return None if modelo is None else self._a_entidad(modelo)

    def leer_todos(
            self, 
    ) -> List[Entidad]:
        """Lee todas las entidades."""

        with self._conexion.transaccion() as sesion:

            query = select(self.modelo).order_by(getattr(self.modelo, "id"))
            
            modelos = sesion.scalars(query).all()
            
            return [
                self._a_entidad(modelo)
                for modelo in modelos
            ]

    def actualizar(
            self,
            entidad: Entidad
            ) -> Entidad:
        """Actualiza una entidad existente."""

        with self._conexion.transaccion() as sesion:

            modelo = sesion.get(
                self.modelo,
                entidad.id
            )

            if modelo is None:
                raise ValueError(f"No existe un registro con id {entidad.id}.")

            self._actualizar_modelo(
                sesion,
                modelo,
                entidad
            )

            sesion.flush()  

            return self._a_entidad(modelo)

    def eliminar(
            self,
            id: int
    ) -> bool:
        """Elimina una entidad por su ID."""
        with self._conexion.transaccion() as sesion:
            
            modelo = sesion.get(
                self.modelo,
                id
            )

            if modelo is None:
                return False

            sesion.delete(modelo)
            return True



        

