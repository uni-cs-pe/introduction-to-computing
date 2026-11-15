#include <stdio.h>

// Escribe el mayor de tres enteros, con decisiones anidadas.
int main(void) {
    int a, b, c;

    if (scanf("%d %d %d", &a, &b, &c) != 3) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (a > b) {
        if (a > c) {
            printf("%d\n", a);
        } else {
            printf("%d\n", c);
        }
    } else {
        if (b > c) {
            printf("%d\n", b);
        } else {
            printf("%d\n", c);
        }
    }

    return 0;
}
