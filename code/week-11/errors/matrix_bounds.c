// Error: una columna que no existe. Los índices se leen de la entrada.
#include <stdio.h>

int main(void) {
    int m[2][3] = {{1, 2, 3}, {4, 5, 6}};
    int j;

    if (scanf("%d", &j) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }
    printf("m[0][%d] = %d\n", j, m[0][j]);
    return 0;
}
