# Keyword_con_Gmail
## Objetivo
Armar un programa en Python, Go, Groovy o Java que pueda acceder, de manera automática, a una cuenta de Gmail, leer los correos e identificar aquellos que tengan la palabra "DevOps" en el Body.

De estos correos identificados, se deberá guardar en una base de datos MySQL los siguientes campos:

· fecha de recepción del correo

· to (remitente que ha enviado el correo)

· subject

Tener en cuenta que solo deberá guardar aquellos correos que ya no haya guardado en alguna corrida anterior.
## Información necesaria para la ejecución
### Librerías

Todas las librerías utilizadas se encuentran integradas en la biblioteca estándar de Python, por lo que no es necesario realizar la instalación por separado. A continuación, se agrega un breve detalle de cada una:

· Imaplib: Protocolo del cliente IMAP4

· Email: Paquete de manejo de correo electrónico y MIME

· Sqlite3: DB-API 2.0 interfaz para bases de datos SQLite

### Módulos y funciones:
Se utilizó la función decode_header que es proporcionada por el módulo email.header, la cual es una API heredada de la librería email (mencionada en el apartado 4.1). A continuación, se agrega un breve detalle de la función utilizada:

· decode_header: Decodifica un valor de encabezado de mensaje sin convertir el juego de caracteres.
## Descripción de la aplicación, problemas y soluciones
### Descripción de la aplicación
Al iniciar la ejecución de la aplicación se solicita al usuario la cuenta de Gmail y contraseña para iniciar la sesión. Una vez iniciada la sesión, realiza la conexión al Servidor de correo entrante (IMAP) de Gmail y busca si existen mails nuevos en la bandeja de entrada.
En caso de identificar nuevos mails, se realiza la búsqueda de la palabra “DevOps” en cada uno de ellos y solo si la encuentra, agrega el registro (campos mencionados en el apartado 3 del presente documento) a la tabla “mails” de la base de datos “KeywordBD”.
En caso de no identificar nuevos mails, la aplicación finaliza su ejecución.

## Problemas y soluciones

Durante el desarrollo de la aplicación surgieron varios errores los cuales fueron solucionados a través del análisis del código e investigación en varias fuentes de casos similares. Los principales fueron los siguientes:

· Contar los mails nuevos: Se definió un contador para recuperar el número de mails que se encontraban como no leídos en la bandeja de entrada, pero en principio realizaba un conteo de todos los mails de la bandeja (leídos y no leídos).

Luego se creó una lista con todos los datos recuperados mediante el método search() de imaplib (mails marcados como “unseen”), se usó el método split() en dicha lista para separar cada elemento dentro de ella y luego mediante len() se contaron estos elementos.

· Encontrar palabra “DevOps”: Para lograr identificar la palabra en el cuerpo del mail se realizaba la búsqueda de coincidencia directamente y no lograba identificarlo correctamente.

Para solucionarlo se usó el método split() para separar por líneas, luego se agregó un for para ir recorriendo cada palabra de cada línea y buscar la coincidencia de “DevOps”.

· Marcar mails como “leídos”: Cada que se ejecutaba la aplicación leía los mails, pero no los marcaba como leídos en el buzón, por lo cual los seguía leyendo en cada ejecución. La solución a esto fue muy sencilla, ya que solo se agregó la instrucción “readonly = False” cuando se selecciona el buzon (Inbox) dentro de la función select() de imaplib.

## Ejecución de la Aplicación

A continuación, se detallan los pasos para iniciar la aplicación “Keyword” y su ejecución:

1. Abrir consola de comandos

2. Cambiar al directorio donde se encuentra el archivo Keyword.py

3. Ingresar “python Keyword.py” y luego presionar “Enter”

4. Ingresar cuenta de Gmail y contraseña.

5. Realizar la búsqueda de nuevos mails. Si no encuentra nuevos mails, muestra el mensaje “No se encontraron emails nuevos”.

6. Guardar nuevos mails en la base de datos. 
Si encuentra nuevos mails, la aplicación muestra la cantidad de mails identificados, y solo agrega a la base de datos aquellos que contienen en el body la palabra “DevOps”. Crea la tabla “mails” (en caso de no existir) e imprime el registro de dicha tabla.
Asimismo, crea el archivo “KeywordBD.db” en el mismo directorio donde se encuentra el script “Keyword.py”.
Si la tabla “mails” ya existe, se muestra un mensaje indicándolo, agrega el nuevo mail identificado y muestra el registro de la tabla “mails”.


