#include <stdio.h>
#include <stdlib.h>

// Lee una semilla y escribe los primeros cinco números de rand con esa semilla.
int main(void) {
    int seed;

    if (scanf("%d", &seed) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (seed < 0) {
        printf("La semilla no puede ser negativa\n");
        return 1;
    }

    srand((unsigned) seed);

    for (int i = 1; i <= 5; i++) {
        printf("%d\n", rand());
    }
    return 0;
}
