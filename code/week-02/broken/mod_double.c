// Error a propósito: % solo funciona con enteros.
#include <stdio.h>

int main(void) {
    double x = 7.5;

    printf("%f\n", x % 2);
    return 0;
}
