#include <stdio.h>

// Lee cuántas temperaturas vienen y luego cada una. Escribe la mayor.
int main(void) {
    int n;

    if (scanf("%d", &n) != 1 || n < 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    int max = 0;  // Este 0 nunca se usa: la primera vuelta lo reemplaza.
    for (int i = 0; i < n; i++) {
        int temperature;
        if (scanf("%d", &temperature) != 1) {
            printf("Entrada inválida\n");
            return 1;
        }
        if (i == 0 || temperature > max) {
            max = temperature;
        }
    }

    printf("La mayor es %d\n", max);
    return 0;
}
