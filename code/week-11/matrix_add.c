// Sumar dos matrices del mismo tamaño, casilla por casilla.
#include <stdio.h>

#define ROWS 2
#define COLS 3

void add_matrices(int a[][COLS], int b[][COLS], int result[][COLS], int rows) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < COLS; j++) {
            result[i][j] = a[i][j] + b[i][j];
        }
    }
}

int main(void) {
    int a[ROWS][COLS] = {{1, 2, 3}, {4, 5, 6}};
    int b[ROWS][COLS] = {{10, 20, 30}, {40, 50, 60}};
    int result[ROWS][COLS];

    add_matrices(a, b, result, ROWS);
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            printf("%3d", result[i][j]);
        }
        printf("\n");
    }
    return 0;
}
