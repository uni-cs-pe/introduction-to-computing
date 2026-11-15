#include <stdio.h>

#define SIZE 4

// Escribe dónde está cada elemento de un arreglo de int.
int main(void) {
    int prices[SIZE] = {350, 1200, 80, 999};

    printf("sizeof(int) = %zu\n", sizeof(int));
    for (int i = 0; i < SIZE; i++) {
        printf("prices[%d] = %4d está en %p\n", i, prices[i], (void *) &prices[i]);
    }
    return 0;
}
