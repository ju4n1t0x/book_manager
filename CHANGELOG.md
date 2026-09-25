# CHANGELOG

## [Ejercicio 4]

- Se crea ServicioCrud con las operaciones comunes y un servicio por entidad con sus validaciones.
- No se pueden borrar géneros, editoriales, monedas o tipos de cotización que estén en uso.
- Al borrar un libro se borran también sus precios y su stock.
- Se agrega DolarApi para consultar las cotizaciones del día con urllib.
- Se agrega CotizadorService para calcular el precio de los libros en pesos según cada tipo de dólar.
- Se agrega ReporteService con los reportes del sistema.

## [Ejercicio 3]

- Se agregan las interfaces IRepositorio, IRepositorioStock e IRepositorioCotizacionDolar.
- Se crea ArchivoCSV para leer y escribir los archivos de datos.
- Se crea RepositorioCSV, un repositorio genérico con el CRUD completo sobre un CSV.
- Se crean los repositorios de cada entidad y los de Stock y CotizacionDolar.
- Se agrega la clase Repositorios que arma todos los repositorios en orden.

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
