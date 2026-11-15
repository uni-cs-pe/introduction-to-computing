// A propósito: sizeof de un parámetro arreglo no da el tamaño del arreglo.
#include <stdio.h>

void print_size(int a[]) {
    printf("en la función: %zu bytes\n", sizeof(a));
}

void print_size_five(int a[5]) {
    printf("con [5] en el parámetro: %zu bytes\n", sizeof(a));
}

int main(void) {
    int grades[5] = {14, 9, 17, 11, 20};

    printf("en main: %zu bytes\n", sizeof(grades));
    print_size(grades);
    print_size_five(grades);
    return 0;
}
