// Error a propósito: el ciclo se detiene cuando aún queda un elemento por mirar.
#include <stdio.h>

#define N 3

int binary_search_wrong(const int a[], int n, int value) {
    int low = 0;
    int high = n - 1;
    while (low < high) {
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
    int a[N] = {10, 20, 30};
    for (int i = 0; i < N; i++) {
        printf("El %d está en el índice %d; responde %d\n", a[i], i,
               binary_search_wrong(a, N, a[i]));
    }
    return 0;
}
