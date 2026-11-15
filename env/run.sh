#!/usr/bin/env bash
# Construye (si hace falta) la imagen del curso y abre una shell en el contenedor
# de trabajo. Es la alternativa a Codespaces para quien usa Docker en su laptop.
#
#   run.sh               abre una shell (si ya está abierta, entra a la misma)
#   run.sh make test     ejecuta un comando dentro del contenedor
#   run.sh --rebuild     reconstruye la imagen
set -euo pipefail

IMAGE=intro-computacion
NAME=intro-computacion
HERE="$(cd "$(dirname "$0")" && pwd)"

build() {
    docker build -t "$IMAGE" -f "$HERE/Dockerfile" "$HERE/.."
}

if [ "${1:-}" = "--rebuild" ]; then
    build
    shift
    [ $# -eq 0 ] && exit 0
elif ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
    build
fi

[ $# -eq 0 ] && set -- bash
TTY=-i; [ -t 0 ] && TTY=-it

if [ "$(docker inspect -f '{{.State.Running}}' "$NAME" 2>/dev/null)" = "true" ]; then
    MOUNT="$(docker inspect -f '{{index .Config.Labels "curso.mount"}}' "$NAME")"
    case "$PWD/" in
        "$MOUNT"/*) WD="$PWD" ;;
        *) echo "Aviso: el contenedor abierto monta $MOUNT; se entra a esa carpeta." >&2; WD="$MOUNT" ;;
    esac
    exec docker exec $TTY -w "$WD" "$NAME" "$@"
fi

# SYS_PTRACE permite usar gdb y valgrind dentro del contenedor.
exec docker run --rm $TTY --name "$NAME" --label "curso.mount=$PWD" \
    --cap-add=SYS_PTRACE --security-opt seccomp=unconfined \
    -v "$PWD":"$PWD" -w "$PWD" "$IMAGE" "$@"
