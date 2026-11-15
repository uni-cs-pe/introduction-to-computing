// Búsqueda lineal: mira los elementos uno por uno, en cualquier orden.
#include <assert.h>
#include <stdio.h>

#define N 6

int linear_search(const int a[], int n, int value) {
    for (int i = 0; i < n; i++) {
        if (a[i] == value) {
            return i;
        }
    }
    return -1;
}

int main(void) {
    int grades[N] = {14, 9, 17, 11, 20, 9};

    assert(linear_search(grades, N, 14) == 0);   // el primero
    assert(linear_search(grades, N, 9) == 1);    // repetido: da el primero que encuentra
    assert(linear_search(grades, N, 13) == -1);  // no está
    assert(linear_search(grades, 0, 14) == -1);  // arreglo vacío

    printf("Buscar 17 devuelve %d\n", linear_search(grades, N, 17));
    printf("Buscar 13 devuelve %d\n", linear_search(grades, N, 13));
    return 0;
}
