#include <stdio.h>

// Prototipo: anuncia la función. Termina en punto y coma y no tiene cuerpo.
int cube(int x);

int main(void) {
    printf("%d\n", cube(3));
    return 0;
}

// Definición: aquí está el cuerpo.
int cube(int x) {
    return x * x * x;
}
