#include <stdio.h>

// Error a propósito: sin break, la ejecución sigue en el case de abajo.
int main(void) {
    int option;
    int price = 0;

    if (scanf("%d", &option) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    switch (option) {
        case 1:
            price = 1200;
        case 2:
            price = 1500;
        case 3:
            price = 1800;
            break;
        default:
            printf("Opción inválida\n");
            return 1;
    }

    printf("Precio: %d céntimos\n", price);
    return 0;
}
