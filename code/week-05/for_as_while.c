#include <stdio.h>

// El mismo ciclo de for_trace.c, escrito con while.
int main(void) {
    int i;

    i = 0;
    while (i < 10) {
        printf("i vale %d\n", i);
        i += 3;
    }

    printf("Al salir, i vale %d\n", i);
    return 0;
}
