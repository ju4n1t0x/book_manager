# Book Manager

Trabajo Práctico Integrador - Seminario de Actualización.

## Sprint actual: Sprint 3

## Objetivo

Scrapping web para obtencion de precios de nuestros competidores.

## Introducción y contexto

### Sprint 2

**Desarrollar el sprint 3**

En esta tercer entrega vamos a descargar y obtener datos de la web para trabajar con ellos.

La idea es obtener precios de nuestros competidores (librerías con venta online) y de esta forma poder compararnos con ellos y competir de forma más informada.

Para todo esto debemos partir del último push que se realizó en la entrega 2.

### Entidades

- **Libro**: cada título del catálogo (isbn, título, autor, editorial, género, año).
- **Genero**: categoría literaria del libro (novela, ensayo, infantil, técnico, etc.).
- **Editorial**: proveedor/distribuidora que provee los libros.
- **Moneda**: monedas en las que se puede expresar un precio (ARS, USD, etc.).
- **TipoCotizacion**: tipos de cotización del dólar (Oficial, Blue, MEP, etc.).
- **Precio**: valor de un libro en una moneda determinada.
- **Stock**: cantidad disponible de cada libro.
- **CotizacionDolar**: registro histórico de las cotizaciones por tipo y fecha.

## Estructura

```
## Ejercicio 01

> Puntos: 1

Inicialización y configuración de la herramienta de versionado. Vamos a trabajar sobre la rama llamada "Sprint_3" y debemos partir de la rama "Sprint_2".

La estructura de directorios es:

```

book_manager/
├── src/
│ └── book_manager/
│ ├── database/
│ │ └── connection.py
│ ├── entities/
│ │ └── entities.py
│ ├── models/
│ │ └── models.py
│ ├── preload_data/
│ │ └── preload_data.py
│ ├── repositories/
│ │ └── repositories.py
│ ├── scraper
│ │ └── (estructura del scraper scrapy)
│ ├── services/
│ │ └── services.py
│ ├── migrations
│ │ ├── csv
│ │ └── sql
│ ├── reportes
│ │ └── (reportes excel generados)
│ ├── ui/
│ │ └── console.py
│ └── main.py
├── .env
├── CHANGELOG.md
├── README.md
└── requirements.txt

````

## Cotización del dólar

Las cotizaciones se obtienen de [DolarApi](https://dolarapi.com) usando urllib de la librería estándar, así que no hace falta instalar nada. Si no hay conexión se usa la última cotización guardada.

## Scrapping web

Los datos sobre precios de libros se obtienen de [CuspideSpider](https://cuspide.com/) usando la libreria scrappy.

## Ejecución

Desde la carpeta src:

```bash
python -m book_manager.main
````

Para volver a cargar los datos iniciales de preload_data.py en migrations/csv (se pierden los cambios hechos):

```bash
python -m book_manager.main --importar
```
