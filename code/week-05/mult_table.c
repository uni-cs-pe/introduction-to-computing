#include <stdio.h>

// Escribe la tabla de multiplicar de un número, del 1 al 12.
int main(void) {
    int n;

    if (scanf("%d", &n) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (n < -1000 || n > 1000) {
        printf("Número fuera de rango\n");
        return 1;
    }

    for (int i = 1; i <= 12; i++) {
        printf("%d x %2d = %d\n", n, i, n * i);
    }

    return 0;
}
