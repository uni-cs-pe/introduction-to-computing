// Tiene un error a propósito: %c también lee el salto de línea.
// Aún no revisa lo que devuelve scanf: eso llega con el if, en la semana 4.
#include <stdio.h>

int main(void) {
    int quantity = 0;
    char size = '?';

    printf("Cantidad: ");
    scanf("%d", &quantity);
    printf("Talla: ");
    scanf("%c", &size);

    printf("Leí %d y un carácter de código %d\n", quantity, size);
    return 0;
}
