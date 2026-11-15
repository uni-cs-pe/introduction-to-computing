// Error: == con dos arreglos compara sus direcciones, no su contenido.
#include <stdio.h>

int main(void) {
    char a[] = "hola";
    char b[] = "hola";

    if (a == b) {
        printf("iguales\n");
    } else {
        printf("distintas\n");
    }
    return 0;
}
