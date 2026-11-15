#include <stdio.h>

// En C, 0 es falso y cualquier otro número es verdadero.
int main(void) {
    int n;

    if (scanf("%d", &n) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (n) {
        printf("%d cuenta como verdadero\n", n);
    } else {
        printf("%d cuenta como falso\n", n);
    }
    printf("!n vale %d\n", !n);

    return 0;
}
