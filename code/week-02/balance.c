// Una variable cambia de valor: la asignación no es una ecuación.
#include <stdio.h>

int main(void) {
    int balance = 10;           // saldo de la tarjeta, en soles
    printf("Saldo inicial: %d\n", balance);

    balance = balance - 3;      // un pasaje
    printf("Después del pasaje: %d\n", balance);

    balance = balance + 5;      // una recarga
    printf("Después de la recarga: %d\n", balance);

    return 0;
}
