#include <stdio.h>

// Intenta intercambiar dos valores. Solo intercambia sus copias.
void try_swap(int a, int b) {
    int temp = a;
    a = b;
    b = temp;
    printf("En try_swap: a = %d, b = %d\n", a, b);
}

int main(void) {
    int a = 3;
    int b = 8;

    try_swap(a, b);
    printf("En main:     a = %d, b = %d\n", a, b);
    return 0;
}
