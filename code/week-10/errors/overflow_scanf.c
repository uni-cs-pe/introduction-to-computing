// A propósito: %s sin límite puede escribir fuera de name.
#include <stdio.h>

int main(void) {
    char name[8];

    if (scanf("%s", name) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }
    printf("Hola, %s\n", name);
    return 0;
}
