# Book Manager

Trabajo Práctico Integrador - Seminario de Actualización.

## Sprint actual: Sprint 1

## Objetivo

Aplicar los conocimientos de programación orientada a objetos y de almacenamiento de datos en archivos para su persistencia.

## Introducción y contexto

Una librería con venta al público necesita modernizar su sistema de gestión de inventario de libros. Debido a la fluctuación en los costos de importación de material bibliográfico, el sistema debe gestionar precios en diferentes monedas y seguir de cerca la cotización del dólar para actualizar sus valores en tiempo real.

El objetivo del sprint es desarrollar una aplicación de consola (CLI) en Python que permita gestionar el inventario de la librería y cotizar los libros según el valor del dólar. Se toma como referencia el sitio [Cúspide](https://www.cuspide.com/).

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
book_manager/
├── src/
│   └── book_manager/
│       ├── entities/
│       │   └── entities.py            # clases de dominio
│       ├── preload_data/
│       │   └── preload_data.py        # datos iniciales, se escriben en migrations/csv
│       ├── repositories/
│       │   └── repositories.py        # persistencia en los archivos CSV
│       ├── services/
│       │   └── services.py            # lógica de negocio y consulta de cotizaciones
│       ├── migrations
│       │   └── csv                    # archivos CSV donde se guardan los datos
│       ├── ui/
│       │   └── console.py             # menús de consola
│       └── main.py
├── CHANGELOG.md
├── README.md
└── requirements.txt
```

## Cotización del dólar

Las cotizaciones se obtienen de [DolarApi](https://dolarapi.com) usando urllib de la librería estándar, así que no hace falta instalar nada. Si no hay conexión se usa la última cotización guardada.

## Ejecución

Desde la carpeta src:

```bash
python -m book_manager.main
```

Para volver a cargar los datos iniciales de preload_data.py en migrations/csv (se pierden los cambios hechos):

```bash
python -m book_manager.main --importar
```
