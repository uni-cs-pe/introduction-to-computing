// Búsqueda binaria: en datos ordenados, descarta la mitad en cada paso.
#include <assert.h>
#include <stdio.h>

#define N 10

// a debe estar ordenado de menor a mayor.
int binary_search(const int a[], int n, int value) {
    int low = 0;
    int high = n - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (a[mid] == value) {
            return mid;
        } else if (a[mid] < value) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return -1;
}

int main(void) {
    int codes[N] = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91};

    assert(binary_search(codes, N, 2) == 0);     // el primero
    assert(binary_search(codes, N, 91) == 9);    // el último
    assert(binary_search(codes, N, 23) == 5);    // uno del medio
    assert(binary_search(codes, N, 1) == -1);    // menor que todos
    assert(binary_search(codes, N, 100) == -1);  // mayor que todos
    assert(binary_search(codes, N, 40) == -1);   // entre dos valores
    assert(binary_search(codes, 0, 2) == -1);    // arreglo vacío
    assert(binary_search(codes, 1, 2) == 0);     // un solo elemento

    printf("Todas las pruebas pasaron\n");
    return 0;
}
