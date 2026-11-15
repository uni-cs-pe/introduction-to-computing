#include <stdio.h>

// Escribe en binario un número de 0 a 255, del bit de mayor peso al de menor peso.
int main(void) {
    int n;

    if (scanf("%d", &n) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (n < 0 || n > 255) {
        printf("Número fuera de rango\n");
        return 1;
    }

    for (int weight = 128; weight >= 1; weight /= 2) {
        if (n >= weight) {
            printf("1");
            n -= weight;
        } else {
            printf("0");
        }
    }

    printf("\n");
    return 0;
}
