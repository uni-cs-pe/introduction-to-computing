// Mide selección y qsort con clock. Lee los tamaños de la entrada, hasta que se acabe.
// Para medir se compila con -O2 y sin sanitizers: make build/fast/sort_times
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_N 100000

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
        int saved = a[i];
        a[i] = a[smallest];
        a[smallest] = saved;
    }
    return comparisons;
}

int is_sorted(const int a[], int n) {
    for (int i = 1; i < n; i++) {
        if (a[i - 1] > a[i]) {
            return 0;
        }
    }
    return 1;
}

int main(void) {
    int original[MAX_N];
    int work[MAX_N];
    srand(2026);
    for (int i = 0; i < MAX_N; i++) {
        original[i] = rand();
    }

    int n;
    printf("%7s %12s %10s %10s  %s\n", "N", "comparac.", "selección", "qsort", "ordenado");
    while (scanf("%d", &n) == 1) {
        if (n < 1 || n > MAX_N) {
            printf("Tamaño inválido: %d\n", n);
            return 1;
        }

        for (int i = 0; i < n; i++) {
            work[i] = original[i];
        }
        clock_t start = clock();
        long long comparisons = selection_sort(work, n);
        clock_t end = clock();
        double selection_seconds = (double) (end - start) / CLOCKS_PER_SEC;
        int ok = is_sorted(work, n);

        for (int i = 0; i < n; i++) {
            work[i] = original[i];
        }
        start = clock();
        qsort(work, n, sizeof(work[0]), compare_ints);
        end = clock();
        double qsort_seconds = (double) (end - start) / CLOCKS_PER_SEC;
        ok = ok && is_sorted(work, n);

        printf("%7d %12lld %9.4fs %9.4fs  ", n, comparisons, selection_seconds, qsort_seconds);
        if (ok) {
            printf("sí\n");
        } else {
            printf("NO\n");
        }
    }
    return 0;
}
