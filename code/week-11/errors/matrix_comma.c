// Error: m[1, 2] no es la casilla de la fila 1 y la columna 2.
#include <stdio.h>

int main(void) {
    int m[3][4] = {{1, 2, 3, 4}, {5, 6, 7, 8}, {9, 10, 11, 12}};

    printf("%d\n", m[1, 2]);
    return 0;
}
