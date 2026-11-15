#include <stdio.h>

// Error a propósito: || necesita una condición completa a cada lado.
int main(void) {
    int option;

    if (scanf("%d", &option) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (option == 1 || 2) {
        printf("Opción 1 o 2\n");
    } else {
        printf("Otra opción\n");
    }

    return 0;
}
