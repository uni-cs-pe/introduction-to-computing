#include <stdio.h>

// Muestra los valores de i en un for con paso 3.
int main(void) {
    int i;

    for (i = 0; i < 10; i += 3) {
        printf("i vale %d\n", i);
    }

    printf("Al salir, i vale %d\n", i);
    return 0;
}
