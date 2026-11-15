// ¿Conviene ordenar antes de buscar? Hace k búsquedas de valores que no están, de dos
// formas. Lee N y después los valores de k. Se compila con -O2 y sin sanitizers.
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_N 100000

struct search_result {
    int index;
    int comparisons;
};

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

struct search_result linear_count(const int a[], int n, int value) {
    struct search_result result = {-1, 0};
    for (int i = 0; i < n; i++) {
        result.comparisons++;
        if (a[i] == value) {
            result.index = i;
            return result;
        }
    }
    return result;
}

struct search_result binary_count(const int a[], int n, int value) {
    struct search_result result = {-1, 0};
    int low = 0;
    int high = n - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        result.comparisons++;
        if (a[mid] == value) {
            result.index = mid;
            return result;
        } else if (a[mid] < value) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return result;
}

int main(void) {
    int original[MAX_N];
    int work[MAX_N];

    int n;
    if (scanf("%d", &n) != 1 || n < 1 || n > MAX_N) {
        printf("Entrada inválida\n");
        return 1;
    }

    // Los pares de 0 a 2n - 2, desordenados. Los impares no están en el arreglo.
    srand(2026);
    for (int i = 0; i < n; i++) {
        original[i] = 2 * i;
    }
    for (int i = n - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        int saved = original[i];
        original[i] = original[j];
        original[j] = saved;
    }

    printf("%7s %15s %12s %10s %10s\n", "k", "lineal", "binaria", "t lineal", "t ordenar");
    int k;
    while (scanf("%d", &k) == 1) {
        long long linear_total = 0;
        clock_t start = clock();
        for (int t = 0; t < k; t++) {
            struct search_result r = linear_count(original, n, 2 * (t % n) + 1);
            assert(r.index == -1);
            linear_total = linear_total + r.comparisons;
        }
        clock_t end = clock();
        double linear_seconds = (double) (end - start) / CLOCKS_PER_SEC;

        for (int i = 0; i < n; i++) {
            work[i] = original[i];
        }
        long long binary_total = 0;
        start = clock();
        qsort(work, n, sizeof(work[0]), compare_ints);
        for (int t = 0; t < k; t++) {
            struct search_result r = binary_count(work, n, 2 * (t % n) + 1);
            assert(r.index == -1);
            binary_total = binary_total + r.comparisons;
        }
        end = clock();
        double sorted_seconds = (double) (end - start) / CLOCKS_PER_SEC;

        printf("%7d %15lld %12lld %9.4fs %9.4fs\n", k, linear_total, binary_total,
               linear_seconds, sorted_seconds);
    }
    return 0;
}
