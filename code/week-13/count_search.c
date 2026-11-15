// Cuenta las comparaciones de cada búsqueda, en tres tamaños.
// Una comparación es mirar un elemento del arreglo y compararlo con el valor buscado.
#include <assert.h>
#include <stdio.h>

#define MAX_N 100000
#define SIZES 3

struct search_result {
    int index;         // dónde está, o -1
    int comparisons;   // cuántos elementos se miraron
};

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

// Prueba todos los valores: los pares están en el arreglo y los impares no.
int binary_worst_case(const int a[], int n) {
    int worst = 0;
    for (int value = -1; value <= 2 * n; value++) {
        struct search_result result = binary_count(a, n, value);
        if (result.comparisons > worst) {
            worst = result.comparisons;
        }
    }
    return worst;
}

// Promedio de comparaciones si el valor sí está, probando cada posición una vez.
double linear_average(const int a[], int n) {
    long long total = 0;
    for (int i = 0; i < n; i++) {
        total = total + linear_count(a, n, a[i]).comparisons;
    }
    return (double) total / n;
}

double binary_average(const int a[], int n) {
    long long total = 0;
    for (int i = 0; i < n; i++) {
        total = total + binary_count(a, n, a[i]).comparisons;
    }
    return (double) total / n;
}

int main(void) {
    int sizes[SIZES] = {1000, 10000, 100000};
    int data[MAX_N];
    for (int i = 0; i < MAX_N; i++) {
        data[i] = 2 * i;   // ordenado, y solo con pares
    }

    assert(linear_count(data, 5, 4).index == 2);
    assert(linear_count(data, 5, 4).comparisons == 3);
    assert(binary_count(data, 5, 4).index == 2);
    assert(binary_count(data, 5, 4).comparisons == 1);

    printf("%8s %8s %8s %8s\n", "N", "lineal", "binaria", "peor");
    for (int s = 0; s < SIZES; s++) {
        int n = sizes[s];
        int missing = 2 * n;   // mayor que todos: no está
        printf("%8d %8d %8d %8d\n", n, linear_count(data, n, missing).comparisons,
               binary_count(data, n, missing).comparisons, binary_worst_case(data, n));
    }
    printf("Promedio con N = 1000, si el valor está: lineal %.2f, binaria %.2f\n",
           linear_average(data, 1000), binary_average(data, 1000));
    return 0;
}
