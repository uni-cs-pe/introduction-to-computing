#include <stdio.h>

// Error a propósito: primero divide y recién después pregunta si n es 0.
int main(void) {
    int n;

    if (scanf("%d", &n) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (10 / n > 1 && n != 0) {
        printf("10 / %d es mayor que 1\n", n);
    } else {
        printf("No se cumple\n");
    }

    return 0;
}
