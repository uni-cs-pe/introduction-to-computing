#include <stdio.h>

// Si n es 0, && no evalúa su lado derecho y la división nunca ocurre.
int main(void) {
    int n;

    if (scanf("%d", &n) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (n != 0 && 10 / n > 1) {
        printf("10 / %d es mayor que 1\n", n);
    } else {
        printf("No se cumple\n");
    }

    return 0;
}
