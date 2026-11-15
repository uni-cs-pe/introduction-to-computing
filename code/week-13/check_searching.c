// Parte de las pruebas del laboratorio: test_lab.py corre esto con sus funciones.
// No hace falta leerlo. Usa argumentos de la línea de comandos, que no vemos en el curso.
#include <stdio.h>
#include <string.h>

#define CAP 300

struct search_result {
    int index;
    int comparisons;
};

int linear_search(const int a[], int n, int value);
int binary_search(const int a[], int n, int value);
struct search_result linear_count(const int a[], int n, int value);
struct search_result binary_count(const int a[], int n, int value);

static int max_halvings(int n) {
    int count = 0;
    while (n > 0) {
        n = n / 2;
        count++;
    }
    return count;
}

// Lleno con pares; los que siguen a n también son pares, para detectar si se pasan de n.
static void fill(int a[], int size) {
    for (int i = 0; i < size; i++) {
        a[i] = 2 * i;
    }
}

static int check_linear(void) {
    int a[CAP];
    fill(a, CAP);
    for (int n = 0; n < CAP; n++) {
        for (int i = 0; i < n; i++) {
            if (linear_search(a, n, a[i]) != i) {
                printf("linear_search: n=%d, no encuentra el índice %d\n", n, i);
                return 1;
            }
        }
        // a[n] existe pero no es parte de los n elementos.
        if (linear_search(a, n, a[n]) != -1 || linear_search(a, n, -1) != -1) {
            printf("linear_search: n=%d, debía devolver -1\n", n);
            return 1;
        }
    }
    int repeated[5] = {7, 3, 7, 3, 7};
    if (linear_search(repeated, 5, 3) != 1) {
        printf("linear_search: con repetidos debe devolver el primero\n");
        return 1;
    }
    int unsorted[5] = {5, 1, 9, 3, 7};
    if (linear_search(unsorted, 5, 1) != 1) {
        printf("linear_search: debe funcionar sin orden\n");
        return 1;
    }
    return 0;
}

static int check_binary(void) {
    int a[CAP];
    fill(a, CAP);
    for (int n = 0; n < CAP; n++) {
        for (int i = 0; i < n; i++) {
            if (binary_search(a, n, a[i]) != i) {
                printf("binary_search: n=%d, no encuentra el índice %d\n", n, i);
                return 1;
            }
            if (binary_search(a, n, a[i] + 1) != -1) {
                printf("binary_search: n=%d, encontró un valor que no está\n", n);
                return 1;
            }
        }
        if (binary_search(a, n, a[n]) != -1 || binary_search(a, n, -1) != -1) {
            printf("binary_search: n=%d, debía devolver -1\n", n);
            return 1;
        }
    }
    int repeated[5] = {1, 3, 3, 3, 9};
    int found = binary_search(repeated, 5, 3);
    if (found < 1 || found > 3) {
        printf("binary_search: con repetidos debe dar uno de los índices\n");
        return 1;
    }
    // Sin orden, una búsqueda binaria no encuentra este 1. Una lineal disfrazada sí.
    int unsorted[5] = {5, 1, 9, 3, 7};
    if (binary_search(unsorted, 5, 1) != -1) {
        printf("binary_search: encontró un valor mirando más de lo que parte a la mitad\n");
        return 1;
    }
    return 0;
}

static int check_linear_count(void) {
    int a[CAP];
    fill(a, CAP);
    for (int n = 0; n < CAP; n++) {
        for (int i = 0; i < n; i++) {
            struct search_result r = linear_count(a, n, a[i]);
            if (r.index != i || r.comparisons != i + 1) {
                printf("linear_count: n=%d, valor en %d: da índice %d y %d comparaciones\n",
                       n, i, r.index, r.comparisons);
                return 1;
            }
        }
        struct search_result r = linear_count(a, n, a[n]);
        if (r.index != -1 || r.comparisons != n) {
            printf("linear_count: n=%d, valor ausente: da índice %d y %d comparaciones\n",
                   n, r.index, r.comparisons);
            return 1;
        }
    }
    return 0;
}

static int check_binary_count(void) {
    int a[CAP];
    fill(a, CAP);
    for (int n = 1; n < CAP; n++) {
        int worst = 0;
        for (int value = -1; value <= 2 * n; value++) {
            struct search_result r = binary_count(a, n, value);
            int expected = (value >= 0 && value < 2 * n && value % 2 == 0) ? value / 2 : -1;
            if (r.index != expected) {
                printf("binary_count: n=%d, valor %d: da índice %d\n", n, value, r.index);
                return 1;
            }
            if (r.comparisons < 1) {
                printf("binary_count: n=%d, valor %d: no contó\n", n, value);
                return 1;
            }
            if (r.comparisons > worst) {
                worst = r.comparisons;
            }
        }
        if (worst != max_halvings(n)) {
            printf("binary_count: n=%d, el peor caso da %d y debe ser %d\n", n, worst,
                   max_halvings(n));
            return 1;
        }
    }
    // Pasos exactos en 0, 2, ..., 18: para el 2 se miran a[4] y a[1], y ahí está.
    struct search_result r = binary_count(a, 10, 2);
    if (r.index != 1 || r.comparisons != 2) {
        printf("binary_count: n=10, valor 2: da índice %d y %d comparaciones; deben ser 1 y 2\n",
               r.index, r.comparisons);
        return 1;
    }
    r = binary_count(a, 0, 2);
    if (r.index != -1 || r.comparisons != 0) {
        printf("binary_count: n=0 debe dar -1 y 0 comparaciones\n");
        return 1;
    }
    // Dos búsquedas seguidas no deben sumar sus cuentas.
    struct search_result again = binary_count(a, 10, 2);
    if (again.comparisons != 2) {
        printf("binary_count: la segunda llamada da %d; cada una debe contar desde 0\n",
               again.comparisons);
        return 1;
    }
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        return 2;
    }
    if (strcmp(argv[1], "linear") == 0) {
        return check_linear();
    }
    if (strcmp(argv[1], "binary") == 0) {
        return check_binary();
    }
    if (strcmp(argv[1], "linear_count") == 0) {
        return check_linear_count();
    }
    if (strcmp(argv[1], "binary_count") == 0) {
        return check_binary_count();
    }
    return 2;
}
