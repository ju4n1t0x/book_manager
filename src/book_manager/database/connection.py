
from contextlib import contextmanager
from typing import Iterator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session


class ConexionDB:

    def __init__(self, url: str):
        self.url = url
        self.engine = create_engine(self.url)

    def connect(self) -> None:
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT version();"))
                db_version = result.scalar()   
                print(f"Conexcion a la base de datos PostgreSQL de Supabase "
                    f"establecida exitosamente con SQLAlchemy. \n"
                    f"Versión de la base de datos: {db_version}")

        except Exception as e:
            print(f"Error al conectar a la base de datos "
                f"PostgreSQL de Supabase: {e}")
            print("Verifica que la contraseña sea la correcta y que la base "
                f"de datos de Supabase esté en funcionamiento.")

    def close(self) -> None:
        self.engine.dispose()

    @contextmanager
    def transaccion(self) -> Iterator[Session]:
        """Context manager para manejar una transacción.

        Hace commit si todo sale bien, rollback si hay un error y siempre
        cierra la sesión.

        Yields:
            Session: Sesión para hacer las operaciones.
        """
        sesion = Session(self.engine, expire_on_commit=False)
        try:
            yield sesion
            sesion.commit()
        except Exception:
            sesion.rollback()
            raise
        finally:
            sesion.close()




