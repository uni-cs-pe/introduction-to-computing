#include <stdio.h>

// Suma los enteros de 1 a n.
int main(void) {
    int n;

    if (scanf("%d", &n) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    int sum = 0;
    int i = 1;
    while (i <= n) {
        sum = sum + i;
        i = i + 1;
    }

    printf("La suma de 1 a %d es %d\n", n, sum);
    return 0;
}
