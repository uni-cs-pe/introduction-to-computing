// Una matriz se guarda fila por fila, con los elementos seguidos.
#include <stdio.h>

#define ROWS 3
#define COLS 4

int main(void) {
    int m[ROWS][COLS] = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 10, 11, 12},
    };

    printf("sizeof(m) = %zu\n", sizeof(m));
    printf("sizeof(m[0]) = %zu\n", sizeof(m[0]));
    printf("sizeof(m[0][0]) = %zu\n", sizeof(m[0][0]));
    printf("m[1][2] = %d\n", m[1][2]);

    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            printf("m[%d][%d] = %2d está en %p\n", i, j, m[i][j], (void *) &m[i][j]);
        }
    }
    return 0;
}
