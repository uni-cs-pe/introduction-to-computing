#include <stdio.h>

// Con (void), una llamada con argumentos es un error de compilación.
int get_year(void) {
    return 2026;
}

int main(void) {
    printf("%d\n", get_year(1, 2, 3));
    return 0;
}
