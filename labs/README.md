# Laboratorio: entorno de trabajo

Todo el curso se trabaja en un mismo entorno, con `gcc`, `gdb`, `make`, Git y Python
3.14. Hay dos formas de abrirlo.

## Opción 1: GitHub Codespaces (la habitual)

Solo requiere un navegador, internet y una cuenta de GitHub, así que funciona en las
computadoras de la universidad. Necesita una conexión estable: si el laboratorio no la tiene,
usen la opción 2, que funciona sin internet una vez construida la imagen.

1. Crear una cuenta en GitHub, con el correo de la universidad si es posible.
2. Abrir el repositorio del curso, en el enlace que da el docente.
3. Elegir **Code → Codespaces → Create codespace**. La primera vez tarda unos minutos.
4. En la terminal de abajo, correr `env/check.sh`. Todas las líneas deben decir `ok`.

Al terminar, cierren la pestaña y detengan el codespace desde
<https://github.com/codespaces>. La cuenta gratuita incluye 120 horas de cómputo al
mes, que en una máquina de 2 núcleos rinden 60 horas de uso, y 15 GB de almacenamiento.
Alcanza para el curso si no dejan el codespace encendido sin usarlo.
Antes de cerrar, descarguen los archivos que tengan que entregar.

## Opción 2: Docker en una laptop

Docker es un programa que hace funcionar, dentro de su laptop, una computadora pequeña con
Linux. A esa computadora se le llama **contenedor**. El del curso ya trae instalado todo
lo que se usa: `gcc`, `gdb`, `make`, Git y Python. Así todos trabajan con las mismas
herramientas, sea cual sea su laptop, y no tienen que instalar nada más.

No necesitan aprender Docker. Para el curso basta con instalarlo una vez y conocer un solo
comando, `bash env/run.sh`, que abre el contenedor.

Necesitan una laptop con Windows 10 u 11, macOS o Linux, unos 3 GB libres en el disco e
internet para la primera vez. Después funciona sin conexión.

### Paso 1: instalar Docker (una sola vez)

**En macOS o Linux**

1. Descarguen e instalen [Docker Desktop](https://docs.docker.com/get-started/get-docker/).
2. Ábranlo y esperen a que diga que está en marcha (*Engine running*). Docker tiene que
   estar abierto cada vez que trabajen.

**En Windows**

En Windows hay un paso más, porque el entorno se usa desde una terminal de Linux. Si
prefieren evitarlo, usen la opción 1.

1. Abran **PowerShell** como administrador (clic derecho → *Ejecutar como administrador*),
   escriban `wsl --install` y reinicien la laptop. Esto instala **Ubuntu**, una terminal de
   Linux dentro de Windows. Al abrirla por primera vez les pide crear un usuario y una
   contraseña.
2. Descarguen e instalen [Docker Desktop](https://docs.docker.com/get-started/get-docker/).
   Si pregunta por WSL 2, acepten.
3. Abran Docker Desktop y, en **Settings → Resources → WSL integration**, activen
   **Ubuntu**.
4. De aquí en adelante, la terminal del curso es **Ubuntu**, que está en el menú de inicio.

**Comprobar la instalación.** Abran una terminal (en Windows, Ubuntu) y escriban:

```text
$ docker --version
Docker version 28.3.2, build 578ccf6
```

El número puede ser otro. Si en cambio dice `command not found`, cierren la terminal y
vuelvan a abrirla; si sigue igual, Docker no quedó instalado.

### Paso 2: descargar la carpeta del curso (una sola vez)

En la terminal, vayan a la carpeta donde quieren guardar el curso y copien el repositorio.
El enlace lo da el docente:

```text
$ git clone <enlace del repositorio>
$ cd <carpeta que se creó>
```

Si su laptop no tiene `git` (pasa en macOS y Linux recién instalados), en la página del
repositorio elijan **Code → Download ZIP**, descompriman el archivo y entren a esa carpeta
con `cd`. En Windows háganlo siempre con `git clone` desde Ubuntu, para que la carpeta
quede del lado de Linux.

Para saber que están en la carpeta correcta, escriban `ls`: deben ver `code`, `env` y
`labs`.

### Paso 3: abrir el contenedor

Con Docker abierto, y desde la carpeta del curso:

```text
$ bash env/run.sh
```

La primera vez descarga y prepara el contenedor. Verán pasar muchas líneas y puede tardar
entre 5 y 10 minutos, según su conexión. No lo interrumpan. Las siguientes veces abre en
un par de segundos.

Saben que están dentro cuando la línea donde escriben cambia y empieza con `root@`:

```text
root@3f2a9c41d7b0:/home/ana/curso#
```

Todo lo que escriban ahí se ejecuta en el contenedor, con las herramientas del curso.

### Paso 4: comprobar que funciona

Dentro del contenedor:

```text
# env/check.sh
ok    gcc compila C17 sin advertencias
ok    el programa en C se ejecuta
...
```

Todas las líneas deben decir `ok`. Si alguna dice `FALLA`, copien el mensaje y avisen al
docente.

> **Córranlo dentro del contenedor, no en la terminal de su laptop.** Fíjense en la línea
> donde escriben: debe empezar con `root@`. Fuera del contenedor, `env/check.sh` no
> comprueba nada y les pide abrir primero el entorno. Lo mismo vale para compilar y
> ejecutar los programas del curso: siempre dentro.

### El trabajo de cada día

1. Abrir Docker Desktop.
2. Abrir la terminal, entrar a la carpeta del curso con `cd` y correr `bash env/run.sh`.
3. Trabajar: compilar y ejecutar en esa terminal.
4. Al terminar, escribir `exit`. Eso cierra el contenedor.

Tres cosas que conviene saber:

- **Sus archivos no se pierden al salir.** La carpeta del curso es la misma dentro y fuera
  del contenedor: lo que guardan dentro queda en su laptop, y al revés.
- **Editen con el editor que prefieran en la laptop**, por ejemplo
  [Visual Studio Code](https://code.visualstudio.com), abriendo la carpeta del curso. El
  contenedor es solo para compilar y ejecutar.
- **Pueden abrir una segunda terminal.** Si corren `bash env/run.sh` otra vez desde la
  carpeta del curso, entran al mismo contenedor.

## Compilar

```sh
gcc -Wall -Wextra -std=c17 -g -fsanitize=address,undefined programa.c -o programa
./programa
```

Cada laboratorio trae un `Makefile`, así que normalmente basta con `make` y `make test`.

## Problemas frecuentes

| Síntoma | Causa | Qué hacer |
|---|---|---|
| El codespace no abre o se desconecta | Conexión o cuota agotada | Revisar la conexión y el uso en <https://github.com/codespaces>; avisar al docente |
| `permission denied` al ejecutar | El archivo no es ejecutable o se llamó sin `./` | `chmod +x archivo` o usar `./programa` |
| `command not found` | Están fuera del entorno | Comprobar que la terminal es la del codespace o del contenedor |
| `env/check.sh` dice "Están fuera del entorno del curso" | Lo corrieron en la terminal de la laptop | Correr `bash env/run.sh` y repetir `env/check.sh` cuando la línea empiece con `root@` |
| `undefined reference to sqrt` | Falta la biblioteca matemática | Agregar `-lm` al final del comando |
| `dubious ownership` de Git | Carpeta de otro usuario | Abrir la carpeta desde `env/run.sh` |
| `docker: command not found` | Docker no está instalado, o la terminal se abrió antes de instalarlo | Cerrar y volver a abrir la terminal; si sigue, repetir el paso 1 |
| `Cannot connect to the Docker daemon` | Docker Desktop está cerrado | Abrir Docker Desktop, esperar a que esté en marcha y repetir el comando |
| `env/run.sh: No such file or directory` | No están en la carpeta del curso | Entrar a la carpeta con `cd`; `ls` debe mostrar `code`, `env` y `labs` |
| `permission denied` al correr `env/check.sh` | El archivo perdió el permiso de ejecución al descomprimir | Correrlo como `bash env/check.sh` |
| En Linux, `permission denied` al usar `docker` | Su usuario no puede usar Docker | Correr `sudo usermod -aG docker $USER`, cerrar sesión y volver a entrar |
| El programa parece colgado | Espera datos de la entrada, o hay un ciclo infinito | Escribir los datos, o `Ctrl+D` para terminar la entrada y `Ctrl+C` para cortarlo |
