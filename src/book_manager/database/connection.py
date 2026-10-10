import os

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator
from dotenv import load_dotenv
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
                print(f"Conexcion a la base de datos PostgreSQL de Supabase establecida exitosamente con SQLAlchemy. \nVersión de la base de datos: {db_version}")

        except Exception as e:
            print(f"Error al conectar a la base de datos PostgreSQL de Supabase: {e}")
            print("Verifica que la contraseña sea la correcta y que la base de datos de Supabase esté en funcionamiento.")

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


class TestConnection:

    @staticmethod
    def test_connection():
        env_path = Path("src/book_manager/.env")
        load_dotenv(dotenv_path=env_path)

        url = os.getenv("DIRECT_URL")

        if not url:
            raise ValueError("La variable de entorno 'DIRECT_URL' no está definida en el archivo .env.")

        db = ConexionDB(url)

        try:
            db.connect()
        finally:
            db.close()

if __name__ == "__main__":
    TestConnection.test_connection()

