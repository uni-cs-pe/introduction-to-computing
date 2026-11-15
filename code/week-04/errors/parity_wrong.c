#include <stdio.h>

// Error a propósito: con negativos, el resto puede ser -1.
int main(void) {
    int n;

    if (scanf("%d", &n) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (n % 2 == 1) {
        printf("%d es impar\n", n);
    } else {
        printf("%d es par\n", n);
    }

    return 0;
}
