# CHANGELOG


## [Ejercicio 7]

- Configuramos la variable `API_URL` en el archivo `.env` para obtener las cotizaciones desde DolarAPI.
- Creamos el servicio `ServicioCotizacionDolar` con la función `obtener_cotizaciones`, encargada de consultar la API, identificar los tipos de cotización y guardar los valores en la base de datos.
- Adaptamos los repositorios `RepositorioTipoCotizacion` y `RepositorioCotizacionDolar` para trabajar con PostgreSQL mediante SQLAlchemy.
- Actualizamos `repositories.py` para utilizar los repositorios de PostgreSQL en las cotizaciones, manteniendo los demás repositorios en CSV.
- Modificamos `main.py` para cargar la variable `DIRECT_URL`, establecer la conexión con PostgreSQL e inicializar los servicios.
- Mantuvimos la compatibilidad con los nombres anteriores para no afectar el funcionamiento del resto del sistema.

## [Ejercicio 6]

- Realizamos la migracion de los repositorios para que empiecen a consumir y persistir los datos directamente en la base de datos de supabase
- Dejamos la migracion de los archivos csv, solo para que se migren al inciar, pero dejan de tener implementacion en el sistema

## [Ejercicio 5]

- Creamos migrations/migrations.py con la función migrar_datos.
- La función lee los csv de migrations/csv y genera un archivo sql por tabla en migrations/sql, respetando el orden de dependencias entre tablas.
- Cargamos los datos en la base dentro de una transacción y ajustamos las secuencias de los ids para que los próximos altas no se repitan.

## [Ejercicio 4]

- Creamos models/models.py con las tablas del sistema usando SQLAlchemy.
- Las tablas tienen los mismos nombres y columnas que los csv del sprint 1.
- Agregamos las relaciones entre las tablas y la función crear_tablas.

## [Ejercicio 3]

- Agregamos a ConexionDB el context manager transaccion para manejar las transacciones.
- Hace commit si sale todo bien, rollback si hay un error y cierra la sesión.

## [Ejercicio 1]

- Creamos la rama para el Sprint 2
- Agregamos a la estructura el directorio y el archivo conenction.py que sera el encargado de gestionar la conexcion a la base de datos
- Modularizamos el resto de los archivos, separando por entidades y logica perteneciente a cada entidad, services separados, repositories separados

## [Ejercicio 2]

- Creamos el projecto en supabase para generar la base de datos.
- Instalamos las dependencias SqlAlchemy y el driver psycopg para poder gestionar la conexcion a supabase a traves del ORM.
- Creamos la clase ConexionDB que es quien se va a encargar de conectarse a la base de datos de supabase a traves de SqlAlchemy.
- Instalamos la dependencia python-dotenv para poder manipular variables de entorno.
- Definimos en .env (en la raiz del proyecto) la variable DIRECT_URL que contendra el enlace + pass para conectarse a la db
- Agregamos al .gitignore el archivo .env para no subir las variables de entorno al repositorio de github
