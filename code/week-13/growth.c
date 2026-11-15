// Cómo crecen N, log N y N²: tablas de números exactos.
#include <assert.h>
#include <stdio.h>

// Cuántas veces se puede partir n a la mitad, sin decimales, hasta llegar a 0.
// Es el máximo de comparaciones de la búsqueda binaria en n elementos.
int halvings(int n) {
    int count = 0;
    while (n > 0) {
        n = n / 2;
        count++;
    }
    return count;
}

void print_row(int n) {
    long long square = (long long) n * n;
    printf("%9d %5d %9d %14lld\n", n, halvings(n), n, square);
}

int main(void) {
    assert(halvings(0) == 0);
    assert(halvings(1) == 1);
    assert(halvings(2) == 2);
    assert(halvings(3) == 2);

    printf("%9s %5s %9s %14s\n", "N", "log", "N", "N*N");
    for (int n = 1000; n <= 8000; n = n * 2) {
        print_row(n);
    }
    printf("\n");
    for (int n = 1000; n <= 1000000; n = n * 10) {
        print_row(n);
    }
    return 0;
}
