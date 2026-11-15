// Mantener un vector: un arreglo con capacidad fija y una longitud que cambia.
#include <stdio.h>

#define CAPACITY 5

void print_vector(const int v[], int n) {
    printf("n = %d:", n);
    for (int i = 0; i < n; i++) {
        printf(" %d", v[i]);
    }
    printf("\n");
}

// Inserta value en la posición pos. Devuelve la longitud nueva.
// Si no se puede, no cambia nada y devuelve la misma longitud.
int insert_at(int v[], int n, int capacity, int pos, int value) {
    if (n >= capacity || pos < 0 || pos > n) {
        return n;
    }
    for (int i = n; i > pos; i--) {
        v[i] = v[i - 1];
    }
    v[pos] = value;
    return n + 1;
}

// Elimina el elemento de la posición pos. Devuelve la longitud nueva.
// Si no se puede, no cambia nada y devuelve la misma longitud.
int remove_at(int v[], int n, int pos) {
    if (pos < 0 || pos >= n) {
        return n;
    }
    for (int i = pos; i < n - 1; i++) {
        v[i] = v[i + 1];
    }
    return n - 1;
}

int main(void) {
    int v[CAPACITY] = {10, 20, 30};
    int n = 3;

    print_vector(v, n);
    n = insert_at(v, n, CAPACITY, 1, 99);
    print_vector(v, n);
    n = insert_at(v, n, CAPACITY, 4, 40);
    print_vector(v, n);
    n = insert_at(v, n, CAPACITY, 0, 5);  // ya está lleno: no cambia
    print_vector(v, n);
    n = remove_at(v, n, 0);
    print_vector(v, n);
    n = remove_at(v, n, 3);
    print_vector(v, n);
    n = remove_at(v, n, 7);               // no existe: no cambia
    print_vector(v, n);
    return 0;
}
