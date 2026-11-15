// Reemplaza rand y srand para las pruebas del laboratorio. No hace falta leerlo.
// rand da 2, 3, 2, 3...: con rand() % 6 + 1, dos dados siempre suman 7.
// srand termina el programa si se llama dos veces.
#include <stdio.h>
#include <stdlib.h>

static int next_value = 2;
static int srand_calls = 0;

int rand(void) {
    int value = next_value;
    next_value = 5 - next_value;
    return value;
}

void srand(unsigned seed) {
    (void) seed;
    srand_calls++;
    if (srand_calls > 1) {
        printf("srand se llamó más de una vez\n");
        exit(3);
    }
}
