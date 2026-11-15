#include <stdio.h>

// Error a propósito: el else va con el if más cercano, no con el de su sangría.
int main(void) {
    int a, b;

    if (scanf("%d %d", &a, &b) != 2) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (a > 0)
        if (b > 0)
            printf("Ambos positivos\n");
    else
        printf("a no es positivo\n");

    return 0;
}
