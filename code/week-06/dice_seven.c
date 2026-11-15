#include <stdio.h>
#include <stdlib.h>

// Lee una semilla y una cantidad de intentos.
// Simula dos dados y estima la probabilidad de que sumen 7.
int main(void) {
    int seed, trials;
    int hits = 0;

    if (scanf("%d %d", &seed, &trials) != 2) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (seed < 0) {
        printf("La semilla no puede ser negativa\n");
        return 1;
    }

    if (trials < 1 || trials > 10000000) {
        printf("Los intentos deben estar entre 1 y 10000000\n");
        return 1;
    }

    srand((unsigned) seed);

    for (int i = 1; i <= trials; i++) {
        int d1 = 1 + rand() % 6;
        int d2 = 1 + rand() % 6;

        if (d1 + d2 == 7) {
            hits++;
        }
    }

    printf("%d intentos, %d sumaron 7, estimación %.4f\n", trials, hits, (double) hits / trials);
    return 0;
}
