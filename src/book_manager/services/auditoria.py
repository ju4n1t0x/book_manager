"""Decorador para registrar las operaciones del sistema."""

from functools import wraps

from book_manager.models.models import AuditoriaModelo


def auditar(accion: str):
    """Registra en la base de datos una operación realizada."""

    def decorador(funcion):
        @wraps(funcion)
        def envoltura(self, *args, **kwargs):
            resultado = funcion(self, *args, **kwargs)

            conexion = self._repositorio._conexion

            detalles = (
                f"Operación: {funcion.__name__}. "
                f"Parámetros: {args}, {kwargs}"
            )

            with conexion.transaccion() as sesion:
                registro = AuditoriaModelo(
                    accion=accion,
                    detalles=detalles,
                )
                sesion.add(registro)

            return resultado

        return envoltura

    return decorador