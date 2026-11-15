#include <stdio.h>

// Calcula y además escribe: solo se puede ver el resultado leyendo la pantalla.
void discount_and_print(int total) {
    if (total >= 10000) {
        total = total - total / 10;
    }
    printf("A pagar: %d.%02d soles\n", total / 100, total % 100);
}

int main(void) {
    int total;

    if (scanf("%d", &total) != 1 || total < 0) {
        printf("Entrada inválida\n");
        return 1;
    }

    discount_and_print(total);
    return 0;
}
