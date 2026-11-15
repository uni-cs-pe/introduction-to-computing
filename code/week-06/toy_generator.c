#include <stdio.h>

// Un generador de juguete: cada número sale del anterior con una fórmula.
// Lee la semilla y escribe 18 números.
int main(void) {
    int x;

    if (scanf("%d", &x) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (x < 0 || x > 15) {
        printf("La semilla debe estar entre 0 y 15\n");
        return 1;
    }

    for (int i = 1; i <= 18; i++) {
        x = (5 * x + 3) % 16;
        printf("%d ", x);
    }
    printf("\n");
    return 0;
}
