// Laboratorio, partes 1 y 2: búsqueda lineal y binaria, y contar comparaciones.
//
// Escriban cada función según su comentario. Borren las líneas (void) de cada una:
// solo están para que el archivo compile sin advertencias mientras tanto.
//
// En main hay una prueba de cada función. Agreguen más con assert: el primero, el
// último, un valor que no está, n igual a 0.
//
// Pruébenlo con make test-lab.
#include <assert.h>
#include <stdio.h>

#define MAX_N 100000
#define SIZES 3

struct search_result {
    int index;         // dónde está, o -1
    int comparisons;   // cuántos elementos se miraron
};

// Devuelve el primer índice donde está value, o -1 si no está.
int linear_search(const int a[], int n, int value) {
    (void) a;
    (void) n;
    (void) value;
    return -1;
}

// a está ordenado de menor a mayor. Devuelve un índice donde está value, o -1.
// Usen low, high y mid, y calculen mid con low + (high - low) / 2.
int binary_search(const int a[], int n, int value) {
    (void) a;
    (void) n;
    (void) value;
    return -1;
}

// Como linear_search, y además cuenta los elementos que miró: uno por cada
// elemento del arreglo que compara con value.
struct search_result linear_count(const int a[], int n, int value) {
    struct search_result result = {-1, 0};
    (void) a;
    (void) n;
    (void) value;
    return result;
}

// Como binary_search, y además cuenta los elementos que miró: uno por cada a[mid].
struct search_result binary_count(const int a[], int n, int value) {
    struct search_result result = {-1, 0};
    (void) a;
    (void) n;
    (void) value;
    return result;
}

int main(void) {
    int small[5] = {10, 20, 30, 40, 50};

    assert(linear_search(small, 5, 50) == 4);
    assert(binary_search(small, 5, 50) == 4);
    assert(linear_count(small, 5, 30).comparisons == 3);
    assert(binary_count(small, 5, 30).comparisons == 1);

    // Con estos datos los pares están y los impares no. 2 * n es mayor que todos.
    int data[MAX_N];
    for (int i = 0; i < MAX_N; i++) {
        data[i] = 2 * i;
    }
    int sizes[SIZES] = {1000, 10000, 100000};
    for (int s = 0; s < SIZES; s++) {
        int n = sizes[s];
        // Escriban aquí una línea con printf("%d %d %d\n", ...): n, las comparaciones
        // de linear_count y las de binary_count, buscando 2 * n en los n primeros.
        (void) n;
        (void) data;
    }

    printf("Todas las pruebas pasaron\n");
    return 0;
}
