#include <stdio.h>

#define SIZE 5

// Formas de inicializar un arreglo.
int main(void) {
    int full[SIZE] = {3, 1, 4, 1, 5};
    int partial[SIZE] = {7, 8};
    int zeros[SIZE] = {0};
    int counted[] = {10, 20, 30};

    for (int i = 0; i < SIZE; i++) {
        printf("i = %d: full %d, partial %d, zeros %d\n",
               i, full[i], partial[i], zeros[i]);
    }

    printf("sizeof(full)    = %zu\n", sizeof(full));
    printf("sizeof(full[0]) = %zu\n", sizeof(full[0]));
    printf("elementos de full    = %zu\n", sizeof(full) / sizeof(full[0]));
    printf("elementos de counted = %zu\n", sizeof(counted) / sizeof(counted[0]));
    return 0;
}
