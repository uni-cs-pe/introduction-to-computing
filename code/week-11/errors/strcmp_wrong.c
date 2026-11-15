// Error: strcmp devuelve 0 si son iguales, y en un if el 0 es falso.
#include <stdio.h>
#include <string.h>

int main(void) {
    char a[] = "hola";
    char b[] = "hola";

    if (strcmp(a, b)) {
        printf("iguales\n");
    } else {
        printf("distintas\n");
    }
    return 0;
}
