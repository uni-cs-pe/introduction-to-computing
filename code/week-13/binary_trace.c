// Muestra los índices de cada paso de la búsqueda binaria.
#include <stdio.h>

#define N 10

int binary_search_trace(const int a[], int n, int value) {
    int low = 0;
    int high = n - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        printf("low = %d, high = %d, mid = %d, a[mid] = %d\n", low, high, mid, a[mid]);
        if (a[mid] == value) {
            return mid;
        } else if (a[mid] < value) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    printf("low = %d, high = %d: ya no queda nada\n", low, high);
    return -1;
}

int main(void) {
    int codes[N] = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91};

    int value;
    if (scanf("%d", &value) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }
    printf("Resultado: %d\n", binary_search_trace(codes, N, value));
    return 0;
}
