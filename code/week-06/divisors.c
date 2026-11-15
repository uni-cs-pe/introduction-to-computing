#include <stdio.h>

// Lee limit. Para cada número de 1 a limit escribe sus divisores y cuántos son.
int main(void) {
    int limit;

    if (scanf("%d", &limit) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (limit < 1 || limit > 1000) {
        printf("El límite debe estar entre 1 y 1000\n");
        return 1;
    }

    for (int n = 1; n <= limit; n++) {
        int count = 0;

        printf("%d:", n);
        for (int d = 1; d <= n; d++) {
            if (n % d == 0) {
                printf(" %d", d);
                count++;
            }
        }
        printf(" (%d)\n", count);
    }
    return 0;
}
