// Ordenamiento por selección: muestra cada pasada y cuenta las comparaciones.
#include <assert.h>
#include <stdio.h>

#define N 5

void print_array(const int a[], int n) {
    for (int i = 0; i < n; i++) {
        printf(" %d", a[i]);
    }
    printf("\n");
}

void swap_at(int a[], int i, int j) {
    int saved = a[i];
    a[i] = a[j];
    a[j] = saved;
}

// Ordena de menor a mayor y devuelve cuántas comparaciones hizo.
long long selection_sort(int a[], int n) {
    long long comparisons = 0;
    for (int i = 0; i < n - 1; i++) {
        int smallest = i;
        for (int j = i + 1; j < n; j++) {
            comparisons++;
            if (a[j] < a[smallest]) {
                smallest = j;
            }
        }
        swap_at(a, i, smallest);
        printf("i = %d, menor en %d:", i, smallest);
        print_array(a, n);
    }
    return comparisons;
}

int main(void) {
    int unsorted[N] = {29, 10, 14, 37, 13};
    int sorted[N] = {10, 13, 14, 29, 37};

    printf("Inicio:");
    print_array(unsorted, N);
    printf("Comparaciones: %lld\n", selection_sort(unsorted, N));

    printf("Inicio:");
    print_array(sorted, N);
    printf("Comparaciones: %lld\n", selection_sort(sorted, N));

    assert(selection_sort(sorted, 0) == 0);
    return 0;
}
