// A propósito: name es pequeño y al lado puede haber otra variable importante.
#include <stdio.h>

int main(void) {
    int is_admin = 0;
    char name[8];

    if (scanf("%s", name) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }
    printf("Hola, %s\n", name);
    if (is_admin != 0) {
        printf("Acceso de administrador (is_admin = %d)\n", is_admin);
    } else {
        printf("Acceso normal\n");
    }
    return 0;
}
