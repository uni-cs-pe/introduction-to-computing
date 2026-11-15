// Error a propósito: búsqueda binaria en un arreglo que no está ordenado.
#include <stdio.h>

#define N 5

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
    int a[N] = {5, 1, 9, 3, 7};
    for (int i = 0; i < N; i++) {
        printf("El %d está en el índice %d; binaria responde %d\n", a[i], i,
               binary_search(a, N, a[i]));
    }
    return 0;
}
