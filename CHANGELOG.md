# CHANGELOG

## [Ejercicio 2]

- Se crea la clase base EntidadBase con el id de las entidades.
- Se crean las entidades Genero, Editorial, Moneda, TipoCotizacion, Libro, Precio, Stock y CotizacionDolar.
- Los atributos son privados y se acceden con properties que validan los datos.
- Libro se relaciona con Editorial y Genero; Precio con Libro y Moneda; Stock con Libro; CotizacionDolar con TipoCotizacion.

## [Ejercicio 1]

- Se crea el repositorio remoto y se sincroniza con el local.
- Se crea la rama Sprint_1.
- Se arma la estructura de carpetas del proyecto con los archivos CHANGELOG.md, README.md y requirements.txt.
- Se corrige la estructura: `repositories/repositories.py` y la carpeta `migrations/csv`.
- Se agrega la carpeta `data` donde se guardan los datos del sistema.
- Se completa el README con el objetivo y el contexto del sprint.
