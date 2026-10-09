# Book Manager

Trabajo Práctico Integrador - Seminario de Actualización.

## Sprint actual: Sprint 2

## Objetivo

Persistir los datos en una base de datos relacional utilizando como ORM SQLAlchemy

## Introducción y contexto

### Sprint 2

**Desarrollar el sprint 2**

En esta segunda entrega vamos a ampliar el alcance haciendo que nuestra aplicación persista en una base de datos relacional. Para este caso vamos a utilizar el ORM [SQLAlchemy](https://colab.research.google.com/drive/1SKsOF5rdQ-Ul4PnMloZsCsNRO2nWH4KZ).

La idea principal es realizar una migración de todos los datos cargados en los archivos a tablas relacionales.

El objetivo principal es consolidar las bases de manejo de bases de datos, normalización, conexión segura y carga inicial.

Además realizaremos consultas a APIs externas.

Para todo esto debemos partir del último push que se realizó en la entrega 1.

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
│       ├── database/
│       │   └── connection.py          # conexcion a la base de datos
│       ├── entities/
│       │   └── entities.py            # clases de dominio
│       ├── preload_data/
│       │   └── preload_data.py        # datos iniciales, se escriben en migrations/csv
│       ├── repositories/
│       │   └── repositories.py        # persistencia en los archivos CSV
│       ├── services/
│       │   └── services.py            # lógica de negocio y consulta de cotizaciones
│       ├── migrations/
│       │   └── csv/                   # archivos CSV donde se guardan los datos
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
