# Introducción
Proyecto inicial para principantes con el stack de Odoo, Docker y Docker Compose.

## Objetivos
- :computer: Establecer un entorno de trabajo básico para seguir el curso.
- :whale2: Favorecer el uso de Docker frente a máquinas virtuales convencionales.
- :package: Recordar cómo hacer copias de directorios con ```tar```.
- :memo: Familiarizarse con Docker Compose y la sintaxis de ```docker-compose.yml```.
- :gear: Entender los distintos componentes de la arquitectura desplegada.

# Primeros pasos

Una vez hayas hecho checkout de este repositorio, en el directorio de tu copia local da permisos de ejecución a los scripts:
```bash
chmod +x *.sh
```

Ejecuta el script ```menu.sh```, la primera vez se autoconfigurará:
```bash
./menu.sh
```

Te pedirá que cierres el terminal y vuelvas a abrir otro.
Regresa a la ruta de tu copia local del repositorio y vuelve a lanzar el menú.
Si no encuentra el paquete ```smenu```, puedes instalarlo (o pedir que lo hagan):
```bash
sudo apt install smenu -y
```

Ahora el menú debería ser interactivo:
```bash
./menu.sh
```

Puedes moverte por el menú utilizando los cursores o directamente el número de la opción que quieras ejecutar. Pulsa _Enter_ para ejecutar la selección.

Para asegurar un correcto acceso a los datos compartidos
mediante volúmenes entre host y contenedores, antes de arrancar o detener contenedores, ejecuta el script que da permisos completos:
```bash
./set-permissions.sh
```

Puedes lanzar los servicios _dockerizados_ en segundo plano con la opción...
```bash
docker-compose up -d
```

... o en primer plano, para poder leer inmediatamente los logs
```bash
docker-compose up
```

Si deseas añadir opciones o documentar las que hay, edita este fichero en cualquier momento:
```bash
nano menu.txt
```

En cada línea que escribas asegúrate de que siga el patrón:
_```comando tabulador # comentario```_

Los cambios que introduzcas en ```menu.txt``` aparecerán como nuevas opciones en el menú interactivo. Este menú está para facilitarte las cosas mientras aprendes, pero a la larga deberás prescindir de él, bien porque ganes soltura con la línea de comandos o bien porque utilices extensiones específicas para Docker desde tu futuro entorno de desarrollo.

# Creación de la primera base de datos en Odoo y backup del entorno

Con ```docker ps``` asegúrate de que los contenedores están corriendo y, si es así, puedes probar a acceder al servicio web de Odoo en su puerto por defecto.
```bash
firefox localhost:8069
```

Configura tu primera base de datos en Odoo en el formulario que aparece.

Según la configuración de volúmenes dada en el fichero ```docker-compose.yml```, los cambios generados en el entorno virtualizado con Docker Compose serán persistentes una vez se detengan y eliminen todos los contenedores. Sin embargo, para asegurar que los ficheros creados sean accesibles desde la máquina anfitriona, es importante que ejecutes el script que da permisos completos:
```bash
./set-permissions.sh
```

Ahora puedes detener y eliminar los contenedores de este entorno
```bash
docker-compose down
```

Es razonable que en ocasiones tengas problemas para acceder desde el la máquina anfitriona a ficheros creados desde un contenedor (o viceversa). Cuando haya importantes cambios en el contenido de los volúmenes compartidos entre host y contenedores, ejecuta ```set-permissions.sh```. 

Dicho script te orientará para que arranques los contenedores y vuelvas a invocarlo si es el único modo de recuperar el acceso completo. Esto es necesario en aquellos equipos en los que no poder ser root ni ejecutar sudo.

Puedes realizar una copia de seguridad de todos los ficheros en este directorio de trabajo:
```bash
tar -czf app.tgz *
```

# Restaurar tu backup

Podrás llevarte ese fichero comprimido con todo tu trabajo a cualquier
entorno con Docker y Docker Compose, preservando instalaciones, configuraciones y datos de Odoo en muy pocos megas.

Para ello, simplemente mueve/copia el fichero ```app.tgz``` a la máquina y ruta de tu elección.

En esa ubicación, desde un terminal, puedes descomprimir el fichero docker-compose.yml y toda la estructura de volúmenes con datos persistentes y ficheros de configuración, para ello ejecuta:
```bash
tar -xvzf app.tgz
```

# Siguientes pasos...

Copia tu fichero ```app.tgz``` a ```/tmp``` y haz las acciones necesarias para desplegar tu entorno desde esa ubicación. Al acceder a Odoo desde el navegador, deberías acceder a la misma base de datos que creaste anteriormente.

Familiarízate con la estructura del fichero ```docker-compose.yml``` y consulta la documentación para entender las palabras clave que observes más habitualmente.

Encuentra la relación que tienen los directorios que ves en este repositorio con las rutas que localizas en el fichero ```docker-compose.yml```.

# Conclusión

Con el fichero ```docker-compose.yml``` estamos definiendo una arquitectura compuesta por varios contenedores. Se comportan como máquinas virtuales ligeras y son completamente independientes, salvo por los recursos que comparten entre sí o con la máquina anfitriona, según lo indicado en el fichero ```docker-compose.yml```: puertos redirigidos, volúmenes, parametrizaciones vía variables de entorno, ...

Este diagrama de componentes se ha generado a partir del  ```docker-compose.yml```, te puede ayudar a visualizar las dependencias entre contenedores los directorios montados como volúmenes y los puertos expuestos y redirigidos a puertos del anfitrión.

![Diagrama docker-compose.yml](https://user-images.githubusercontent.com/1954675/209989973-c7b12c7c-a915-4426-94d0-847274f2bb97.png)
