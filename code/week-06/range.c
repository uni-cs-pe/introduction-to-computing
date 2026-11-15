#include <stdio.h>
#include <stdlib.h>

// Lee un mínimo, un máximo y una semilla. Escribe diez números en ese rango.
int main(void) {
    int min, max, seed;

    if (scanf("%d %d %d", &min, &max, &seed) != 3) {
        printf("Entrada inválida\n");
        return 1;
    }

    // Con estos límites, max - min + 1 no pasa de 32767, el menor RAND_MAX permitido.
    if (min > max || min < -10000 || max > 10000) {
        printf("Rango inválido\n");
        return 1;
    }

    if (seed < 0) {
        printf("La semilla no puede ser negativa\n");
        return 1;
    }

    srand((unsigned) seed);

    for (int i = 1; i <= 10; i++) {
        printf("%d ", min + rand() % (max - min + 1));
    }
    printf("\n");
    return 0;
}
