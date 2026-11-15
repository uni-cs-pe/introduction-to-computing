// Cuánto ocupa cada tipo y cuáles son los límites de los enteros.
#include <limits.h>
#include <stdio.h>

int main(void) {
    printf("bits en un byte: %d\n", CHAR_BIT);
    printf("sizeof(char)   = %zu\n", sizeof(char));
    printf("sizeof(int)    = %zu\n", sizeof(int));
    printf("sizeof(double) = %zu\n", sizeof(double));
    printf("INT_MAX = %d\n", INT_MAX);
    printf("INT_MIN = %d\n", INT_MIN);
    return 0;
}
