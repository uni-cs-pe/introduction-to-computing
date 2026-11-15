#include <stdio.h>

#define SIZE 5

// Bug: i <= SIZE lee un elemento más de los que tiene el arreglo.
int main(void) {
    int grades[SIZE] = {14, 9, 17, 11, 20};
    int sum = 0;

    for (int i = 0; i <= SIZE; i++) {
        printf("grades[%d] = %d\n", i, grades[i]);
        sum = sum + grades[i];
    }
    printf("Suma: %d\n", sum);
    return 0;
}
