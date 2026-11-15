// Error: dentro de una función, == no da ninguna advertencia. Sigue comparando direcciones.
#include <stdio.h>

int same_text(const char a[], const char b[]) {
    return a == b;
}

int main(void) {
    char a[] = "hola";
    char b[] = "hola";

    printf("a con b: %d\n", same_text(a, b));
    printf("a con a: %d\n", same_text(a, a));
    return 0;
}
