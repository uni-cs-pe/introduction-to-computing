#include <stdio.h>

// Error a propósito: el mayor empieza en 0, que no es un dato de la entrada.
int main(void) {
    int n;

    if (scanf("%d", &n) != 1 || n < 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    int max = 0;
    for (int i = 0; i < n; i++) {
        int temperature;
        if (scanf("%d", &temperature) != 1) {
            printf("Entrada inválida\n");
            return 1;
        }
        if (temperature > max) {
            max = temperature;
        }
    }

    printf("La mayor es %d\n", max);
    return 0;
}
