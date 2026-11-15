// Error: el parámetro no dice cuántas columnas tiene la matriz.
#include <stdio.h>

int first(int m[][]) {
    return m[0][0];
}

int main(void) {
    int m[2][3] = {{1, 2, 3}, {4, 5, 6}};

    printf("%d\n", first(m));
    return 0;
}
