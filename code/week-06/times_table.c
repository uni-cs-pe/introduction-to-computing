#include <stdio.h>

// Lee n y escribe la tabla de multiplicar de n por n, de 1 a 12.
int main(void) {
    int n;

    if (scanf("%d", &n) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (n < 1 || n > 12) {
        printf("n debe estar entre 1 y 12\n");
        return 1;
    }

    for (int row = 1; row <= n; row++) {
        for (int col = 1; col <= n; col++) {
            printf("%4d", row * col);
        }
        printf("\n");
    }
    return 0;
}
