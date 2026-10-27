# CHANGELOG

## [Ejercicio 6]
- Incorporamos un decorador para registrar las operaciones del sistema en la tabla de auditoría, almacenando la acción, la fecha y los detalles de cada operación.

## [Ejercicio 5]

- Agregamos la comparación de precios entre el catálogo interno y los resultados obtenidos de Cúspide.
- Agregamos la exportación de la comparación de precios a un archivo Excel.
- Agregamos la opción para exportar el informe desde el menú de reportes.
- Implementamos openpyxl como dependencia para generar archivos Excel.

## [Ejercicio 4]

- Implementamos alerta_precio_service.py para generar alertas de precio al comparar los precios de Cuspide con los de nuestra db
- main_scraper.py pide la diferencia minima de precio en pesos y el tipo de cotizacion del dolar, que se obtiene desde la API configurada en el .env
- Las alertas generadas se guardan en un csv dentro de la carpeta reportes

## [Ejercicio 3]

- Implementamos la estructura del scraper segun los ejercicios planteados
- Implementamos un main_scraper.py para poder ejecutar el scraping web
- Se implementan loaders, middlewares y pipelines para controlar la ejecuccion de cuspide_spider
- El scraper realiza la busqueda con un maximo de match de 10 titulos segun los titulos que tenemos en nuestra db, luego corrobora que el titulo sea el mismo y ademas filtra
  por autor antes de guardar los resultados en reportes.csv

## [Ejercicio 2]

- La funcion sql para importacion de datos se encuentra creada desde el Sprint_2

## [Ejercicio 1]

- Creamos la rama Sprint_3 a partir de la rama Sprint_2
- Creamos la carpeta "scrapper" dentro de los directorios del proyecto
- Creamos la carpeta reportes para guardar los reportes en csv generados
