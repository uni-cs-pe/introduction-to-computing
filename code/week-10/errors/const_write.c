// A propósito: una función con const en el parámetro intenta cambiar el arreglo.
#include <stdio.h>

void reset(const int a[], int n) {
    for (int i = 0; i < n; i++) {
        a[i] = 0;
    }
}

int main(void) {
    int grades[3] = {14, 9, 17};

    reset(grades, 3);
    printf("%d\n", grades[0]);
    return 0;
}
