// const en un parámetro: la función promete que no cambia el arreglo.
#include <stdio.h>

#define N 5

// Requiere n >= 1.
int max_value(const int a[], int n) {
    int max = a[0];
    for (int i = 1; i < n; i++) {
        if (a[i] > max) {
            max = a[i];
        }
    }
    return max;
}

int main(void) {
    int grades[N] = {14, 9, 17, 11, 20};

    printf("Nota mayor: %d\n", max_value(grades, N));
    return 0;
}
