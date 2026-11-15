#include <stdio.h>

// Evalúa las dos formas de cada ley de De Morgan con los valores leídos.
int main(void) {
    int x, y;

    if (scanf("%d %d", &x, &y) != 2) {
        printf("Entrada inválida\n");
        return 1;
    }

    printf("!(x >= 0 && y < 10) vale %d\n", !(x >= 0 && y < 10));
    printf("x < 0 || y >= 10    vale %d\n", x < 0 || y >= 10);
    printf("!(x == 0 || y == 0) vale %d\n", !(x == 0 || y == 0));
    printf("x != 0 && y != 0    vale %d\n", x != 0 && y != 0);

    return 0;
}
