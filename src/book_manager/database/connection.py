from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def _mensaje_integridad(error: IntegrityError) -> str:
    """Traduce una violación de integridad a un mensaje legible.

    Args:
        error: Error de integridad lanzado por la base de datos.

    Returns:
        str: Mensaje para mostrar al usuario.
    """
    detalle = getattr(error.orig, "diag", None)
    restriccion = getattr(detalle, "constraint_name", None) or ""

    if restriccion.endswith("_key"):
        return "Ya existe un registro con esos datos."
    if restriccion.endswith("_fkey"):
        return "El registro referencia un dato que no existe."
    return "Los datos violan una regla de integridad de la base."


class ConexionDB:
    """Maneja el motor de SQLAlchemy y las transacciones del sistema."""

    def __init__(self, url: str) -> None:
        """Inicializa el motor de conexión a la base de datos.

        No abre conexión todavía: SQLAlchemy conecta de forma diferida
        en el primer uso del motor.

        Args:
            url: Cadena de conexión de SQLAlchemy (la `DIRECT_URL` de
                Supabase, por ejemplo).
        """
        self.url = url
        self.engine = create_engine(self.url)

    def connect(self) -> None:
        """Verifica la conexión consultando la versión del servidor.

        Abre una conexión, consulta y la cierra: no queda nada abierto.

        Raises:
            SQLAlchemyError: Si no se puede establecer la conexión.
        """
        with self.engine.connect() as connection:
            db_version = connection.execute(text("SELECT version();")).scalar()

        print(
            "Conexión a PostgreSQL establecida con SQLAlchemy.\n"
            f"Versión de la base de datos: {db_version}"
        )

    def close(self) -> None:
        """Cierra el pool de conexiones del motor.

        Libera las conexiones abiertas por `self.engine`. Una vez
        cerrado, el motor no debería reutilizarse.
        """
        self.engine.dispose()

    @contextmanager
    def transaccion(self) -> Iterator[Session]:
        """Context manager para manejar una transacción.

        Hace commit si todo sale bien, rollback si hay un error y siempre
        cierra la sesión.

        Yields:
            Session: Sesión para hacer las operaciones.

        Raises:
            ValueError: Si la base rechaza los datos por una restricción
                de integridad (clave duplicada o referencia inexistente).
        """
        sesion = Session(self.engine, expire_on_commit=False)
        try:
            yield sesion
            sesion.commit()
        except IntegrityError as error:
            sesion.rollback()
            raise ValueError(_mensaje_integridad(error)) from error
        except Exception:
            sesion.rollback()
            raise
        finally:
            sesion.close()



