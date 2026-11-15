// Pasa un arreglo a una función: la longitud va en otro parámetro.
#include <stdio.h>

#define N 5

int sum(int a[], int n) {
    int total = 0;
    for (int i = 0; i < n; i++) {
        total = total + a[i];
    }
    return total;
}

int main(void) {
    int grades[N] = {14, 9, 17, 11, 20};

    int total = sum(grades, N);
    printf("Suma de las 5 notas: %d\n", total);
    printf("Promedio: %.2f\n", (double) total / N);
    printf("Suma de las 3 primeras: %d\n", sum(grades, 3));
    return 0;
}
