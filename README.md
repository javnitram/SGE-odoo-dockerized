# Introducción
Proyecto inicial para principantes con el stack de Odoo, PostgreSQL, PgAdmin4, Docker y Docker Compose.

## Contenidos
- [Introducción](#introducción)
  - [Contenidos](#contenidos)
- [Objetivos](#objetivos)
- [Primeros pasos](#primeros-pasos)
- [Acceso a Odoo, creación de la primera base de datos en Odoo y consulta desde PgAdmin4](#acceso-a-odoo-creación-de-la-primera-base-de-datos-en-odoo-y-consulta-desde-pgadmin4)
- [Entendiendo la configuración del almacenamiento persistente](#entendiendo-la-configuración-del-almacenamiento-persistente)
- [Gestión de backups](#gestión-de-backups)
- [Siguientes pasos...](#siguientes-pasos)
- [Conclusión](#conclusión)

# Objetivos

- :computer: Establecer un entorno de trabajo básico para seguir el curso.
- :whale2: Favorecer el uso de Docker frente a máquinas virtuales convencionales.
- :memo: Familiarizarse con Docker Compose y la sintaxis de ```docker-compose.yml```.
- :gear: Entender los distintos componentes de la arquitectura desplegada.
- :package: Adquirir soltura para hacer backups y poder restaurarlos en casa.

# Primeros pasos

Una vez hayas hecho checkout de este repositorio, en el directorio de tu copia local da permisos de ejecución al script ```menu.sh```:

```bash
chmod +x menu.sh
```

Ejecuta el script ```menu.sh```:

```bash
./menu.sh
```

Si no encuentra el paquete ```smenu```, puedes instalarlo (o pedir que lo hagan si no eres administrador):

```bash
sudo apt install smenu -y
```

Si el paquete está instalado, el menú debería ser interactivo:

```bash
./menu.sh
```

Puedes moverte por el menú utilizando los cursores (:arrow_up:, :arrow_down:) o directamente el número de la opción que quieras ejecutar. Pulsa _Enter_ para ejecutar la selección.

Si estás en el aula, ejecuta...

```bash
set_permissions
```

... para dar los permisos adecuados a los directorios y ficheros que usarán los contenedores.

Puedes lanzar los servicios en segundo plano con la opción...

```bash
docker compose up -d
```

Para ver su salida, puedes usar la opción...

```bash
docker compose logs -f
```

... con ```Control + C``` puedes interrumpir el comando sin parar los servicios.

También puedes levantar los contenedores en primer plano para ver su salida inmediatamente, el comando es el mismo, omitiendo la opción ```-d``` o ```--detach```...

```bash
docker compose up
```

...pero recuerda, que en este caso, con ```Control + C``` estarás interrumpiendo los servicios.

Si deseas añadir opciones al menú o documentar las que hay, edita el fichero ```menu.txt``` en cualquier momento:

```bash
nano menu.txt
```

En cada línea que escribas asegúrate de que siga el patrón:
_```comando tabulador # comentario```_

Los cambios que introduzcas en ```menu.txt``` aparecerán como nuevas opciones en el menú interactivo. Si tienes problemas en la visualización de opciones, ajusta el tamaño de ventana, revisa la sintaxis del fichero, el uso de tabuladores o almohadillas.

> [!NOTE]
> Este menú está para facilitarte las cosas mientras aprendes, pero a la larga prescindirás de él, bien porque ganes soltura con la línea de comandos o bien porque utilices extensiones específicas para Docker desde el entorno de desarrollo que usaremos más adelante en el curso.

# Acceso a Odoo, creación de la primera base de datos en Odoo y consulta desde PgAdmin4

Con ```docker ps``` o ```docker compose ps``` asegúrate de que los contenedores están corriendo. 

Accede a la aplicación web de Odoo, aprovechando que el fichero ```docker-compose.yml``` tiene configurados varios reenvíos de puertos.
```bash
firefox localhost:8069
```

Configura tu primera base de datos en Odoo en el formulario que aparece.

En otra pestaña del navegador, accede a PgAdmin4. Puedes encontrar el puerto de escucha, las credenciales de acceso de PgAdmin y las del usuario de base de datos de Odoo configuradas en el fichero ```docker-compose.yml```.

> [!IMPORTANT]
> Tómate un tiempo en conocer el fichero de configuración ```docker-compose.yml```.

# Entendiendo la configuración del almacenamiento persistente

Hay tres tipos de almacenamiento en Docker:

- **volumes**: Docker almacena los datos dentro de un área del sistema de ficheros gestionada por él, sólo Docker tiene permisos sobre esta ubicación. **Es el mecanismo preferido para hacer persistentes los datos**. En Linux, los volúmenes se almacenan en ```/var/lib/docker/volumes/```, ningún proceso aparte de Docker debería modificarlos. Un volumen puede ser montado por diferentes contenedores a la vez.
- **bind mounts**: Son puntos de montaje que mapean cualquier fichero o directorio del sistema de ficheros anfitrión dentro de un contenedor. A diferencia de los volúmenes, a través de este mecanismo es posible acceder a la ruta mapeada y modificar los ficheros desde fuera del contenedor.
- **tmpfs**: Se trata de un almacenamiento temporal en memoria, no se guarda en el sistema de ficheros. Se suele utilizar para el almacenamiento de información sensible.

![](https://docs.docker.com/storage/images/types-of-mounts.png)

En el fichero ```docker-compose.yml```, has podido observar varios bloques **volumes**. Hay uno al final del fichero (a nivel principal de la sintaxis YAML) y otros anidados (a nivel servicios donde se usan). Estos bloques **volumes** no se corresponden exclusivamente con ese tipo de almacenamiento.

El bloque **volumes** del nivel principal sí define volúmenes propiamente dichos, es decir, almacenamiento persistente gestionado por Docker. En este bloque se declaran volúmenes para que puedan ser configurados en el bloque **volumes** del servicio donde queremos usarlos. Por ejemplo, se declara un volumen con nombre ```pgdata``` y se configura dentro del servicio ```db``` como ```pgdata:/var/lib/postgresql/data/pgdata``` para que el contenedor tenga almacenamiento persistente en la ruta **/var/lib/postgresql/data/pgdata**.

Sin embargo, en el bloque volumes a nivel de otros servicios, puedes ver la configuración de otro tipo de almacenamiento persistente, en particular, de **bind mounts**. Para bien o para mal, este mecanismo permitiría modificar el sistema de ficheros del anfitrión desde el contenedor, con las implicaciones de seguridad que ello conlleva. A su vez, **bind mounts** sí permiten que los ficheros del contenedor se modifiquen desde el anfitrión y se consideran apropiados para compartir ficheros de configuración y código, como es el caso de este proyecto. Por ejemplo, la línea ```./odoo/addons:/mnt/extra-addons``` mapea la ruta relativa **odoo/addons** de este proyecto dentro el contenedor ```odoo``` en la ruta **/mnt/extra-addons**.

Dada la naturaleza de los **bind mounts**, es razonable que en ocasiones tengas problemas para acceder desde el anfitrión a ficheros creados desde un contenedor (o viceversa). Cuando haya nuevos ficheros en las rutas mapeadas con este tipo de almacenamiento, ejecuta la opción **set_permissions** del script ```menu.sh```.

# Gestión de backups

El script ```menu.sh``` proporciona la funcionalidad para exportar e importar tu entorno, de modo que puedas hacer backups o llevarte tu trabajo a casa. Para gestionar backups, se recomienda que detengas todos los servicios:

```bash
docker compose down
```

La opción **save_backup** del script ```menu.sh``` guarda el estado de los volúmenes así como el contenido del directorio de trabajo en un fichero con prefijo ```backup```, seguido del nombre del directorio de trabajo en minúsculas, fecha, hora y nombre de host y extensión .tgz. Cuando guardamos un nuevo backup se genera/actualizado un enlace duro con el mismo nombre del fichero generado, pero reemplazando la fecha y hora por la palabra **latest**. Por ejemplo, el último backup del directorio de trabajo **/home/alumno/Escritorio/SGE-prueba/** del host **pcdam-10** se llamará
**backup_sge-prueba_latest_pcdam-10.tgz**.

La opción **restore_backup** del script ```menu.sh``` restaura la copia de seguridad a partir del backup seleccionado por el usuario entre una lista de posibles opciones. La copia de seguridad puede restaurarse en el mismo host o en otro, pero es necesario que el directorio de trabajo se llame como el directorio original, por ejemplo el fichero **backup_sge-prueba_latest_pcdam-10.tgz** debe restaurarse en el directorio **SGE-prueba** o **sge-prueba**. Aquellos ficheros que no cumplan esta nomenclatura no serán opciones elegibles en **restore_backup**.

Si al copiar tu fichero de backup olvidaste copiar ficheros menu.sh o menu.txt, puedes recuperarlos desde el propio fichero .tgz con el siguiente comando...
```bash
tar -xvzf backup_*latest*.tgz menu.sh menu.txt
```

... y así poder ejecutar el script ```menu.sh```.

Con esta funcionalidad, podrás llevarte todo tu trabajo a cualquier entorno con Docker y Docker Compose, preservando código, configuraciones y datos de tus prácticas en muy pocos megas. Esta funcionalidad utiliza la utilidad [vackup](https://github.com/BretFisher/docker-vackup) para guardar y restaurar backups de volúmenes.

# Siguientes pasos...

Haz una copia de seguridad de un entorno en el que ya hayas configurado una primera base de datos de Odoo. Crea una ruta dentro de ```/tmp``` y haz todas las acciones necesarias para restaurar ahí tu copia de seguridad y desplegar tu entorno desde esa ubicación. Al acceder a Odoo desde el navegador, deberías acceder a la misma base de datos que creaste anteriormente.

Si en casa tienes una máquina con Linux o has instalado [Docker Desktop con WSL2 en Windows](https://docs.docker.com/desktop/install/windows-install/) puedes probar a llevarte tu entorno.

# Conclusión

Con el fichero ```docker-compose.yml``` estamos definiendo una arquitectura compuesta por varios contenedores. Se comportan como máquinas virtuales ligeras y son completamente independientes, salvo por los recursos que comparten entre sí o con la máquina anfitriona, según lo indicado en el fichero ```docker-compose.yml```: puertos redirigidos, volúmenes, parametrizaciones vía variables de entorno, ...

Este diagrama de componentes se ha generado a partir del fichero ```docker-compose.yml```, te puede ayudar a visualizar las dependencias entre contenedores, los volúmenes y los puertos expuestos y redirigidos a puertos del anfitrión.

![Diagrama docker-compose.yml](https://github.com/javnitram/SGE-odoo-dockerized/assets/1954675/6d973dfa-6c5f-43aa-b12e-ea7d7dab7cd5)
