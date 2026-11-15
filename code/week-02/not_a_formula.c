// Una asignación guarda un valor una vez: no deja una fórmula viva.
#include <stdio.h>

int main(void) {
    int price = 2;
    int total = price * 3;      // total recibe 6, no la fórmula

    price = 10;                 // total no se entera de este cambio

    printf("price = %d\n", price);
    printf("total = %d\n", total);
    return 0;
}
