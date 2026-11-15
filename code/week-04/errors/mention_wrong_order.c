#include <stdio.h>

// Error a propósito: la primera rama cierta gana, y aquí va primero la más amplia.
int main(void) {
    int average;

    if (scanf("%d", &average) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (average >= 11) {
        printf("Regular\n");
    } else if (average >= 14) {
        printf("Bueno\n");
    } else if (average >= 17) {
        printf("Excelente\n");
    } else {
        printf("Insuficiente\n");
    }

    return 0;
}
