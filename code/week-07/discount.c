#include <stdio.h>

// Solo calcula: recibe céntimos y devuelve céntimos. Desde 100 soles, 10 % menos.
int price_after_discount(int total) {
    if (total >= 10000) {
        return total - total / 10;
    }
    return total;
}

// Solo escribe.
void print_price(int cents) {
    printf("A pagar: %d.%02d soles\n", cents / 100, cents % 100);
}

// Lee, llama y escribe.
int main(void) {
    int total;

    if (scanf("%d", &total) != 1 || total < 0) {
        printf("Entrada inválida\n");
        return 1;
    }

    print_price(price_after_discount(total));
    return 0;
}
