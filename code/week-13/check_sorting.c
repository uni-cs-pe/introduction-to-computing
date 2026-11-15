// Parte de las pruebas del laboratorio: test_lab.py corre esto con sus funciones.
// No hace falta leerlo. Reemplaza a clock por un reloj de prueba, con un valor conocido,
// para comprobar la medición sin depender de la máquina, y a qsort por una versión que
// se deja contar. Por eso usa variables globales, que en el resto del curso no se usan.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

long long selection_sort(int a[], int n);
int is_sorted(const int a[], int n);
double seconds_selection(int a[], int n);
double seconds_qsort(int a[], int n);

#define N 50
#define BIG 70000

static int *watched;
static int clock_calls;
static int sorted_at_call[8];
static int qsort_calls;

static int really_sorted(const int a[], int n) {
    for (int i = 1; i < n; i++) {
        if (a[i - 1] > a[i]) {
            return 0;
        }
    }
    return 1;
}

// Reloj de prueba: cada llamada avanza medio segundo y anota si el arreglo ya estaba ordenado.
clock_t clock(void) {
    if (clock_calls < 8 && watched != NULL) {
        sorted_at_call[clock_calls] = really_sorted(watched, N);
    }
    clock_calls++;
    return (clock_t) (clock_calls * (CLOCKS_PER_SEC / 2));
}

// Reemplazo de qsort: ordena por inserción con la función que recibe, y cuenta la llamada.
void qsort(void *base, size_t count, size_t size, int (*compare)(const void *, const void *)) {
    qsort_calls++;
    char *bytes = base;
    char saved[64];
    if (size > sizeof(saved)) {
        abort();
    }
    for (size_t i = 1; i < count; i++) {
        memcpy(saved, bytes + i * size, size);
        size_t j = i;
        while (j > 0 && compare(bytes + (j - 1) * size, saved) > 0) {
            memcpy(bytes + j * size, bytes + (j - 1) * size, size);
            j--;
        }
        memcpy(bytes + j * size, saved, size);
    }
}

static void fill_shuffled(int a[], int n) {
    // Una permutación fija de 0..n-1, sin rand.
    for (int i = 0; i < n; i++) {
        a[i] = (i * 37 + 11) % n;
    }
}

static int check_sort(void) {
    int cases[][6] = {{3, 1, 2, 0, 0, 0}, {1, 1, 1, 1, 1, 1}, {6, 5, 4, 3, 2, 1},
                      {1, 2, 3, 4, 5, 6}, {-5, 2000000000, -2000000000, 0, 7, -5}};
    int sizes[] = {3, 6, 6, 6, 6};
    for (int c = 0; c < 5; c++) {
        int n = sizes[c];
        int a[8];
        int reference[8];
        for (int i = 0; i < n; i++) {
            a[i] = cases[c][i];
            reference[i] = cases[c][i];
        }
        // Dos casillas de más que no se deben tocar.
        a[n] = -999;
        a[n + 1] = 999;
        for (int i = 0; i < n - 1; i++) {
            for (int j = i + 1; j < n; j++) {
                if (reference[j] < reference[i]) {
                    int s = reference[i];
                    reference[i] = reference[j];
                    reference[j] = s;
                }
            }
        }
        long long count = selection_sort(a, n);
        for (int i = 0; i < n; i++) {
            if (a[i] != reference[i]) {
                printf("selection_sort: caso %d, posición %d: da %d y debe ser %d\n", c, i, a[i],
                       reference[i]);
                return 1;
            }
        }
        if (a[n] != -999 || a[n + 1] != 999) {
            printf("selection_sort: caso %d, escribió después de n\n", c);
            return 1;
        }
        if (count != (long long) n * (n - 1) / 2) {
            printf("selection_sort: caso %d, %lld comparaciones; deben ser %d\n", c, count,
                   n * (n - 1) / 2);
            return 1;
        }
    }
    int one[1] = {4};
    if (selection_sort(one, 1) != 0 || one[0] != 4) {
        printf("selection_sort: con un elemento debe dar 0 comparaciones\n");
        return 1;
    }
    if (selection_sort(one, 0) != 0) {
        printf("selection_sort: con n = 0 debe dar 0 comparaciones\n");
        return 1;
    }
    return 0;
}

static int check_is_sorted(void) {
    int up[4] = {1, 2, 2, 3};
    int last_bad[4] = {1, 2, 3, 0};
    int first_bad[4] = {5, 1, 2, 3};
    if (is_sorted(up, 4) != 1 || is_sorted(up, 1) != 1 || is_sorted(up, 0) != 1) {
        printf("is_sorted: dice que no a un arreglo ordenado\n");
        return 1;
    }
    if (is_sorted(last_bad, 4) != 0 || is_sorted(first_bad, 4) != 0) {
        printf("is_sorted: dice que sí a un arreglo desordenado\n");
        return 1;
    }
    if (is_sorted(last_bad, 3) != 1) {
        printf("is_sorted: miró más allá de n\n");
        return 1;
    }
    return 0;
}

static int check_seconds(double (*measure)(int[], int), const char *name, int expected_qsort) {
    int a[N];
    fill_shuffled(a, N);
    if (really_sorted(a, N)) {
        return 2;
    }
    watched = a;
    clock_calls = 0;
    qsort_calls = 0;
    double seconds = measure(a, N);
    watched = NULL;
    if (qsort_calls != expected_qsort) {
        printf("%s: llamó a qsort %d veces; debe ser %d\n", name, qsort_calls, expected_qsort);
        return 1;
    }
    if (clock_calls != 2) {
        printf("%s: llamó a clock %d veces; deben ser 2\n", name, clock_calls);
        return 1;
    }
    if (sorted_at_call[0]) {
        printf("%s: ordenó antes de empezar a medir\n", name);
        return 1;
    }
    if (!sorted_at_call[1]) {
        printf("%s: la segunda medición llegó antes de terminar de ordenar\n", name);
        return 1;
    }
    if (seconds < 0.499 || seconds > 0.501) {
        printf("%s: con un reloj que avanza 0.5 s da %f\n", name, seconds);
        return 1;
    }
    return 0;
}

static int check_big_count(void) {
    // No cabe en un int. Se compila con -O2 y sin sanitizers para que tarde poco.
    static int a[BIG];
    fill_shuffled(a, BIG);
    long long count = selection_sort(a, BIG);
    long long expected = (long long) BIG * (BIG - 1) / 2;
    if (count != expected) {
        printf("selection_sort: con %d elementos da %lld y debe ser %lld\n", BIG, count, expected);
        return 1;
    }
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        return 2;
    }
    if (strcmp(argv[1], "sort") == 0) {
        return check_sort();
    }
    if (strcmp(argv[1], "is_sorted") == 0) {
        return check_is_sorted();
    }
    if (strcmp(argv[1], "seconds_selection") == 0) {
        return check_seconds(seconds_selection, "seconds_selection", 0);
    }
    if (strcmp(argv[1], "seconds_qsort") == 0) {
        return check_seconds(seconds_qsort, "seconds_qsort", 1);
    }
    if (strcmp(argv[1], "big_count") == 0) {
        return check_big_count();
    }
    return 2;
}
