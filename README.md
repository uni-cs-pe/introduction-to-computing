# Introducción a la Computación

Código y entorno de trabajo del curso. Los apuntes, las guías de cada semana y las
diapositivas están en el sitio: <https://introduction-to-computing.uni-cs-pe.com>.

## Empezar

Todo el curso se trabaja en un mismo entorno, ya preparado. Hay dos formas de abrirlo y
están explicadas paso a paso en [labs/README.md](labs/README.md):

- **GitHub Codespaces**, desde el navegador: **Code → Codespaces → Create codespace**.
- **Docker** en una laptop: `env/run.sh`.

Con el entorno abierto, corran `env/check.sh`. Todas las líneas deben decir `ok`.

## Qué hay aquí

| Carpeta | Contenido |
|---|---|
| `code/week-NN/` | Los ejemplos de la semana y, en `lab/`, los archivos del laboratorio |
| `env/` | El entorno del curso: `Dockerfile`, `run.sh` y `check.sh` |
| `labs/` | Cómo abrir el entorno y qué hacer si algo falla |

Semanas con código: [1](code/week-01/) · [2](code/week-02/) · [3](code/week-03/) · [4](code/week-04/) · [5](code/week-05/) · [6](code/week-06/) · [7](code/week-07/) · [9](code/week-09/) · [10](code/week-10/) · [11](code/week-11/) · [12](code/week-12/) · [13](code/week-13/) · [14](code/week-14/) · [15](code/week-15/).

En la carpeta de una semana, `make` compila los ejemplos y `make test` corre sus pruebas.
