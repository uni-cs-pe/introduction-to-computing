#include <stdio.h>

// Lee filas y columnas, y dibuja un rectángulo de asteriscos.
int main(void) {
    int rows, cols;

    if (scanf("%d %d", &rows, &cols) != 2) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (rows < 1 || cols < 1) {
        printf("Filas y columnas deben ser positivas\n");
        return 1;
    }

    for (int row = 1; row <= rows; row++) {
        for (int col = 1; col <= cols; col++) {
            printf("*");
        }
        printf("\n");
    }
    return 0;
}
