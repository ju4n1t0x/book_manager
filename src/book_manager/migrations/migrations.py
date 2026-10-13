"""Migración de los datos de los archivos CSV a la base de datos."""

import csv
import datetime
import os
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from sqlalchemy import Column, Table, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Session

from book_manager.database.connection import ConexionDB
from book_manager.models.models import Base, crear_tablas


def _convertir_valor(valor: str, columna: Column) -> Any:
    """Convierte un texto del csv al tipo de dato de la columna.

    Args:
        valor (str): Texto leído del archivo csv.
        columna (Column): Columna de la tabla a la que pertenece el valor.

    Returns:
        Any: Valor convertido (int, Decimal, date o str según la columna).
    """
    tipo = columna.type.python_type
    if tipo is datetime.date:
        return datetime.date.fromisoformat(valor)
    return tipo(valor)


def _leer_csv(ruta: Path, tabla: Table) -> List[Dict[str, Any]]:
    """Lee un archivo csv y convierte cada fila a los tipos de la tabla.

    Args:
        ruta (Path): Ruta del archivo csv.
        tabla (Table): Tabla de la base de datos que representa el archivo.

    Returns:
        List[Dict[str, Any]]: Una fila por registro, con la forma
            {nombre_columna: valor}.
    """
    with open(ruta, encoding="utf-8-sig", newline="") as archivo:
        return [
            {
                nombre: _convertir_valor(valor, tabla.columns[nombre])
                for nombre, valor in fila.items()
            }
            for fila in csv.DictReader(archivo)
        ]


def _generar_sql(tabla: Table, filas: List[Dict[str, Any]]) -> str:
    """Genera el script sql con un INSERT por cada fila.

    Args:
        tabla (Table): Tabla en la que se insertan los registros.
        filas (List[Dict[str, Any]]): Registros a insertar.

    Returns:
        str: Contenido del archivo sql.
    """
    lineas = [f"-- Datos de la tabla {tabla.name}"]
    for fila in filas:
        sentencia = (
            postgresql.insert(tabla).values(fila).on_conflict_do_nothing()
        )
        sql = sentencia.compile(
            dialect=postgresql.dialect(),
            compile_kwargs={"literal_binds": True},
        )
        lineas.append(f"{sql};")
    return "\n".join(lineas) + "\n"


def _ajustar_secuencia(sesion: Session, tabla: Table) -> None:
    """Actualiza la secuencia del id de la tabla.

    Los registros se insertan con el id que traen los csv, y eso no avanza
    la secuencia. Sin este ajuste, el próximo alta intentaría usar un id que
    ya existe.

    Args:
        sesion (Session): Sesión abierta dentro de la transacción.
        tabla (Table): Tabla cuya secuencia se actualiza.
    """
    columna = tabla.autoincrement_column
    if columna is None:
        return
    sesion.execute(
        text(
            f"SELECT setval(pg_get_serial_sequence('{tabla.name}', "
            f"'{columna.name}'), COALESCE(MAX({columna.name}), 0) + 1, false) "
            f"FROM {tabla.name}"
        )
    )


def migrar_datos(carpeta_csvs: str, carpeta_sqls: str) -> None:
    """ Función encargada de la migración de datos de csv a sql.
    Se encarga de leer los archivos csv y crear los archivos sql
    para la inserción en la base de datos.

    Cada tabla se busca en un archivo csv con su mismo nombre. Se procesan
    respetando las dependencias entre tablas (primero las que no dependen
    de otras) y todo se hace en una única transacción: si algo falla no
    queda nada cargado. Se puede ejecutar más de una vez porque los
    registros que ya existen se ignoran.

    Args:
        carpeta_csvs (str): Carpeta donde se encuentran los archivos csv
            de origen.
        carpeta_sqls (str): Carpeta donde se deben guardar los archivos
            sql generados.
    """
    load_dotenv()
    url = os.getenv("DIRECT_URL")
    if not url:
        raise ValueError(
            "La variable de entorno 'DIRECT_URL' no está definida "
            "en el archivo .env."
        )

    Path(carpeta_sqls).mkdir(parents=True, exist_ok=True)
    conexion = ConexionDB(url)
    try:
        crear_tablas(conexion.engine)
        with conexion.transaccion() as sesion:
            tablas = enumerate(Base.metadata.sorted_tables, start=1)
            for orden, tabla in tablas:
                ruta_csv = Path(carpeta_csvs) / f"{tabla.name}.csv"
                if not ruta_csv.exists():
                    continue
                filas = _leer_csv(ruta_csv, tabla)
                if not filas:
                    continue

                ruta_sql = Path(carpeta_sqls) / f"{orden:02d}_{tabla.name}.sql"
                ruta_sql.write_text(
                    _generar_sql(tabla, filas), encoding="utf-8"
                )

                sesion.execute(
                    postgresql.insert(tabla).on_conflict_do_nothing(), filas
                )
                _ajustar_secuencia(sesion, tabla)
                print(f"{tabla.name}: {len(filas)} registros migrados.")
    finally:
        conexion.close()


if __name__ == "__main__":
    carpeta_base = Path(__file__).parent
    migrar_datos(str(carpeta_base / "csv"), str(carpeta_base / "sql"))