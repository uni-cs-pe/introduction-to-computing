// Error: C no dice si dos literales iguales están en el mismo lugar.
#include <stdio.h>

int main(void) {
    printf("%d\n", "hola" == "hola");
    return 0;
}
