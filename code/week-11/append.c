// Agregar al final de una cadena sin pasarse del tamaño del arreglo.
#include <stdio.h>
#include <string.h>

#define BIG 20
#define SMALL 8

// strncat agrega como máximo el número que recibe, y después siempre pone '\0'.
// Por eso se le da lo que queda libre, sin contar el byte del '\0'.
void safe_append(char dest[], const char src[], int size) {
    int used = (int) strlen(dest);
    strncat(dest, src, size - used - 1);
}

int main(void) {
    char big[BIG] = "Ana";
    char small[SMALL] = "Ana";

    safe_append(big, " Quispe", BIG);
    printf("%s\n", big);
    safe_append(small, " Quispe", SMALL);
    printf("%s\n", small);
    return 0;
}
