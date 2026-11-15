// El espacio antes de %c salta los espacios y saltos de línea pendientes.
// Aún no revisa lo que devuelve scanf: eso llega con el if, en la semana 4.
#include <stdio.h>

int main(void) {
    int quantity = 0;
    char size = '?';

    printf("Cantidad: ");
    scanf("%d", &quantity);
    printf("Talla: ");
    scanf(" %c", &size);

    printf("Leí %d y la talla %c\n", quantity, size);
    return 0;
}
