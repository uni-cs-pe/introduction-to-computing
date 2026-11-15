#!/usr/bin/env bash
# Comprueba que el entorno del curso funciona. Todas las líneas deben decir "ok".
set -u

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
status=0

check() {
    local name="$1"; shift
    if "$@" >"$tmp/out" 2>&1; then
        echo "ok    $name"
    else
        echo "FALLA $name"; sed 's/^/      /' "$tmp/out"; status=1
    fi
}

cat >"$tmp/hola.c" <<'C'
#include <stdio.h>

int main(void) {
    printf("hola\n");
    return 0;
}
C
cat >"$tmp/overflow.c" <<'C'
int main(void) {
    int a[2] = {0, 0};
    volatile int i = 2;
    return a[i];
}
C

check "gcc compila C17 sin advertencias" gcc -Wall -Wextra -Werror -std=c17 -o "$tmp/hola" "$tmp/hola.c"
check "el programa en C se ejecuta" "$tmp/hola"
check "el sanitizer compila" gcc -g -fsanitize=address,undefined -o "$tmp/overflow" "$tmp/overflow.c"
check "el sanitizer detecta un error de memoria" bash -c "! '$tmp/overflow'"
check "make" make --version
check "gdb" gdb --version
check "git" git --version
check "Python 3.14" python3 -c 'import sys; assert sys.version_info[:2] == (3, 14)'

exit $status
