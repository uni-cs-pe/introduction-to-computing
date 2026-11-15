#include <stdio.h>

// Lee n y escribe n filas: la fila 3 tiene 1 2 3, y así las demás.
int main(void) {
    int n;

    if (scanf("%d", &n) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (n < 1 || n > 30) {
        printf("n debe estar entre 1 y 30\n");
        return 1;
    }

    for (int row = 1; row <= n; row++) {
        for (int col = 1; col <= row; col++) {
            printf("%3d", col);
        }
        printf("\n");
    }
    return 0;
}
