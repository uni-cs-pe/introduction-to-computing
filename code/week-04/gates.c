#include <stdio.h>

// Las cuatro compuertas, para dos bits a y b (cada uno 0 o 1).
int main(void) {
    int a, b;

    if (scanf("%d %d", &a, &b) != 2) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (a < 0 || a > 1 || b < 0 || b > 1) {
        printf("Los bits deben ser 0 o 1\n");
        return 1;
    }

    printf("AND %d\n", a && b);
    printf("OR  %d\n", a || b);
    printf("NOT %d\n", !a);
    printf("XOR %d\n", a != b);

    return 0;
}
