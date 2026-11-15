// Pasar una matriz a una función: las columnas van en el tipo, las filas en un parámetro.
#include <stdio.h>

#define COLS 4

void print_matrix(int m[][COLS], int rows) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < COLS; j++) {
            printf("%3d", m[i][j]);
        }
        printf("\n");
    }
}

int column_sum(int m[][COLS], int rows, int column) {
    int total = 0;
    for (int i = 0; i < rows; i++) {
        total = total + m[i][column];
    }
    return total;
}

// Como con un arreglo, la función trabaja sobre la matriz original.
void add_bonus(int m[][COLS], int rows, int bonus) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < COLS; j++) {
            m[i][j] = m[i][j] + bonus;
        }
    }
}

int main(void) {
    int grades[3][COLS] = {
        {14, 9, 17, 12},
        {11, 16, 8, 13},
        {18, 10, 15, 20},
    };

    print_matrix(grades, 3);
    printf("Suma del curso 0: %d\n", column_sum(grades, 3, 0));
    printf("Suma del curso 0, solo 2 filas: %d\n", column_sum(grades, 2, 0));
    add_bonus(grades, 2, 1);
    print_matrix(grades, 3);
    return 0;
}
