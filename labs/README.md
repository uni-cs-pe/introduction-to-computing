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

1. Instalar [Docker](https://docs.docker.com/get-started/get-docker/).
2. En la carpeta del curso, correr `env/run.sh`. La primera vez construye la imagen.
3. Dentro del contenedor, correr `env/check.sh`. Todas las líneas deben decir `ok`.

Se edita con cualquier editor en la laptop, porque la carpeta es la misma dentro y fuera
del contenedor.

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
| `undefined reference to sqrt` | Falta la biblioteca matemática | Agregar `-lm` al final del comando |
| `dubious ownership` de Git | Carpeta de otro usuario | Abrir la carpeta desde `env/run.sh` |
| El programa parece colgado | Espera datos de la entrada, o hay un ciclo infinito | Escribir los datos, o `Ctrl+D` para terminar la entrada y `Ctrl+C` para cortarlo |
