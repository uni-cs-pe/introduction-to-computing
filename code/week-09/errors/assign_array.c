#include <stdio.h>

// No compila: un arreglo no se asigna con =.
int main(void) {
    int original[3] = {1, 2, 3};
    int copy[3];

    copy = original;
    printf("%d\n", copy[0]);
    return 0;
}
