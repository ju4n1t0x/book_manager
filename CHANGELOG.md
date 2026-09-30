# CHANGELOG

## [Ejercicio 7]

- Se crea main.py que arma los repositorios, los servicios y la consola.
- main(import_default_data=True) o el parámetro --importar escriben los datos iniciales en migrations/csv.
- Se saca el ajuste de sys.path; el programa se ejecuta desde la carpeta src.
- Se ajusta todo el código a PEP 8 (líneas de hasta 79 caracteres) y los comentarios quedan solo en los docstrings.

## [Ejercicio 6]

- Implementación completa de las interfaces gráficas de consola (CLI) para la gestión CRUD de todas las entidades (Libros, Géneros, Editoriales, Monedas, Precios, Stock, Cotizaciones y Reportes).
- Se crea la consola con el menú principal y un menú CRUD por entidad.
- Se agrega el decorador manejar_errores para mostrar los errores sin cortar el programa.
- Se agregan las funciones para pedir datos por teclado con validación.
- Se agrega el menú de reportes: cotización de un libro, catálogo en pesos, stock bajo e histórico de cotizaciones.
- Al iniciar se actualizan las cotizaciones del día desde DolarApi.
- Se corrigen el alta y la modificación de editoriales (faltaban país y sitio web) y se agrega la descripción de los géneros.

## [Ejercicio 5]

- preload_data.py contiene los datos iniciales y cargar_datos_iniciales los escribe en migrations/csv.
- Se completan géneros, editoriales y monedas hasta 10 registros.
- Se agregan 5 libros con sus precios y su stock; los precios de esos libros quedan en USD para poder cotizarlos.
- Las cotizaciones iniciales son reales, tomadas de api.argentinadatos.com.

## [Ejercicio 4]

- Se crea ServicioCrud con las operaciones comunes y un servicio por entidad con sus validaciones.
- No se pueden borrar géneros, editoriales, monedas o tipos de cotización que estén en uso.
- Al borrar un libro se borran también sus precios y su stock.
- Se agrega DolarApi para consultar las cotizaciones del día con urllib.
- Se agrega CotizadorService para calcular el precio de los libros en pesos según cada tipo de dólar.
- Se agrega ReporteService con los reportes del sistema.
- Se agregan los movimientos de stock (reponer y descontar) y el reporte de stock bajo.

## [Ejercicio 3]

- Se agregan las interfaces IRepositorio, IRepositorioStock e IRepositorioCotizacionDolar.
- Se crea ArchivoCSV para leer y escribir los archivos de datos.
- Se crea RepositorioCSV, un repositorio genérico con el CRUD completo sobre un CSV.
- Se crean los repositorios de cada entidad y los de Stock y CotizacionDolar.
- Se agrega la clase Repositorios que arma todos los repositorios en orden.
- Los repositorios guardan los datos en los archivos de migrations/csv.

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
- Se completa el README con el objetivo y el contexto del sprint.
- Se ajusta la estructura a la de la consigna: se quitan la carpeta `data` y los archivos `__init__.py`.
