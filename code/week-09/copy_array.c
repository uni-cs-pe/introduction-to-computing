#include <stdio.h>

#define SIZE 4

// Copia un arreglo elemento por elemento y cambia solo la copia.
int main(void) {
    int original[SIZE] = {5, 6, 7, 8};
    int copy[SIZE];

    for (int i = 0; i < SIZE; i++) {
        copy[i] = original[i];
    }
    copy[0] = 99;

    printf("original[0] = %d, copy[0] = %d\n", original[0], copy[0]);
    return 0;
}
