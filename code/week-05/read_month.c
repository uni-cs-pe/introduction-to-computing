#include <stdio.h>

// Pide un mes hasta que esté entre 1 y 12. Si no se puede leer un número, termina.
int main(void) {
    int month;

    do {
        if (scanf("%d", &month) != 1) {
            printf("Entrada inválida\n");
            return 1;
        }
        if (month < 1 || month > 12) {
            printf("Mes fuera de rango, escriba otro\n");
        }
    } while (month < 1 || month > 12);

    printf("Mes elegido: %d\n", month);
    return 0;
}
