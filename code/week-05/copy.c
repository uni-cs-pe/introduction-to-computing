#include <stdio.h>

// Copia la entrada en la salida, byte por byte, con la forma corta del ciclo.
int main(void) {
    int c;

    while ((c = getchar()) != EOF) {
        putchar(c);
    }

    return 0;
}
