# CHANGELOG

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
