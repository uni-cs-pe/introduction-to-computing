#include <stdio.h>

// Lee y valida en una sola condición: si scanf falla, n no se llega a mirar.
int main(void) {
    int n;

    if (scanf("%d", &n) == 1 && n >= 1 && n <= 12) {
        printf("Mes válido: %d\n", n);
    } else {
        printf("Mes inválido\n");
        return 1;
    }

    return 0;
}
