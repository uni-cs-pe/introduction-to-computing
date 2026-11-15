#include <stdio.h>

// Devuelve x al cuadrado.
int square(int x) {
    int result = x * x;
    return result;
}

int main(void) {
    int n;

    if (scanf("%d", &n) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    int answer = square(n);
    printf("%d al cuadrado es %d\n", n, answer);
    printf("%d\n", square(2) + square(n + 1));
    return 0;
}
