// Error: la función espera 3 columnas y la matriz tiene 4.
#include <stdio.h>

int first(int m[][3]) {
    return m[0][0];
}

int main(void) {
    int m[2][4] = {{1, 2, 3, 4}, {5, 6, 7, 8}};

    printf("%d\n", first(m));
    return 0;
}
