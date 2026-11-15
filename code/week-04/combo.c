#include <stdio.h>

// Precio en céntimos de un menú según la opción elegida.
int main(void) {
    int option;
    int price;

    if (scanf("%d", &option) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    switch (option) {
        case 1:
            price = 1200;
            break;
        case 2:
            price = 1500;
            break;
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
