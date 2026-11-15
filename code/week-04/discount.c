#include <stdio.h>

// Lee el total de una compra en céntimos. Desde 100 soles se descuenta el 10 %.
int main(void) {
    int total;

    if (scanf("%d", &total) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (total < 0) {
        printf("El total no puede ser negativo\n");
        return 1;
    }

    if (total >= 10000) {
        total = total - total / 10;
    }

    printf("A pagar: %d.%02d soles\n", total / 100, total % 100);
    return 0;
}
