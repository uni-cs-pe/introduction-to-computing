// Muestra los bytes de dos cadenas iguales guardadas en arreglos de distinto tamaño.
#include <stdio.h>

int main(void) {
    char s[] = "hola";
    char t[8] = "hola";

    printf("sizeof(s) = %zu\n", sizeof(s));
    for (int i = 0; i < (int) sizeof(s); i++) {
        printf("s[%d] = %d\n", i, s[i]);
    }
    printf("sizeof(t) = %zu\n", sizeof(t));
    for (int i = 0; i < (int) sizeof(t); i++) {
        printf(" %d", t[i]);
    }
    printf("\n");
    printf("'\\0' vale %d y '0' vale %d\n", '\0', '0');
    return 0;
}
