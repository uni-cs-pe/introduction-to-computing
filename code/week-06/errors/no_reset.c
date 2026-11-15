#include <stdio.h>

// ERROR: col no vuelve a 1 al empezar cada fila.
int main(void) {
    int row = 1;
    int col = 1;

    while (row <= 3) {
        while (col <= 4) {
            printf("*");
            col++;
        }
        printf("\n");
        row++;
    }
    return 0;
}
