#include <stdio.h>

// Guarda cinco notas en un arreglo, cambia dos y las escribe.
int main(void) {
    int grades[5] = {14, 9, 17, 11, 20};

    grades[1] = 12;
    grades[4] = grades[4] - 1;

    for (int i = 0; i < 5; i++) {
        printf("grades[%d] = %d\n", i, grades[i]);
    }
    return 0;
}
