#include <stdio.h>

// Error a propósito: el ; después del if termina la decisión.
int main(void) {
    int n;

    if (scanf("%d", &n) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (n > 0);
    printf("%d es positivo\n", n);

    return 0;
}
