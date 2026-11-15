// qsort ordena un arreglo: le decimos qué tamaño tiene y cómo comparar dos elementos.
#include <stdio.h>
#include <stdlib.h>

#define N 6

// La forma de esta función la pide qsort. Devuelve un número negativo si el primero
// va antes, positivo si va después, y 0 si da igual.
int compare_ints(const void *first, const void *second) {
    int x = *(const int *) first;
    int y = *(const int *) second;
    if (x < y) {
        return -1;
    } else if (x > y) {
        return 1;
    }
    return 0;
}

int main(void) {
    int grades[N] = {14, 9, 17, 11, 20, 9};

    qsort(grades, N, sizeof(grades[0]), compare_ints);

    for (int i = 0; i < N; i++) {
        printf(" %d", grades[i]);
    }
    printf("\n");
    return 0;
}
