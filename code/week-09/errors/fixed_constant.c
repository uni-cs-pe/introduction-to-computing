#include <stdio.h>

// Bug: el índice 5 es constante y está fuera del arreglo.
int main(void) {
    int values[5] = {1, 2, 3, 4, 5};

    values[5] = 99;
    printf("%d\n", values[0]);
    return 0;
}
