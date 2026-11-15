// Laboratorio, parte 3: ordenamiento por selección, y medir con clock.
//
// Escriban cada función según su comentario. Borren las líneas (void) de cada una.
// Pruébenlo con make test-lab. Para medir de verdad, usen make measure: compila con
// -O2 y sin sanitizers. Los tiempos dependen de la máquina; la tendencia, no.
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_N 100000

// La función de comparar que pide qsort. Viene lista.
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

// Ordena de menor a mayor por selección. Devuelve cuántas comparaciones entre elementos
// hizo. Usen long long para contar: con 100 000 elementos, la cuenta no cabe en un int.
long long selection_sort(int a[], int n) {
    (void) a;
    (void) n;
    return 0;
}

// Devuelve 1 si a está ordenado de menor a mayor, y 0 si no.
int is_sorted(const int a[], int n) {
    (void) a;
    (void) n;
    return 0;
}

// Ordena a con selection_sort y devuelve los segundos que tardó, medidos con clock.
double seconds_selection(int a[], int n) {
    (void) a;
    (void) n;
    return 0.0;
}

// Ordena a con qsort y compare_ints, y devuelve los segundos que tardó, medidos con clock.
double seconds_qsort(int a[], int n) {
    (void) a;
    (void) n;
    return 0.0;
}

int main(void) {
    int small[5] = {29, 10, 14, 37, 13};
    assert(selection_sort(small, 5) == 10);
    assert(is_sorted(small, 5) == 1);

    int original[MAX_N];
    int work[MAX_N];
    srand(2026);
    for (int i = 0; i < MAX_N; i++) {
        original[i] = rand();
    }

    // Lee los tamaños de la entrada, hasta que se acabe. Este main viene listo.
    int n;
    while (scanf("%d", &n) == 1) {
        if (n < 1 || n > MAX_N) {
            printf("Tamaño inválido: %d\n", n);
            return 1;
        }
        for (int i = 0; i < n; i++) {
            work[i] = original[i];
        }
        double selection = seconds_selection(work, n);
        int ok = is_sorted(work, n);

        for (int i = 0; i < n; i++) {
            work[i] = original[i];
        }
        double library = seconds_qsort(work, n);
        ok = ok && is_sorted(work, n);

        printf("%d %.4f %.4f ", n, selection, library);
        if (ok) {
            printf("ordenado\n");
        } else {
            printf("NO ORDENADO\n");
        }
    }
    return 0;
}
