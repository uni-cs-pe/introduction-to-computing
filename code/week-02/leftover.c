// Lo que scanf no pudo leer se queda en la entrada, esperando a la siguiente lectura.
#include <stdio.h>

int main(void) {
    // Revisar si la lectura funcionó requiere if: llega en la semana 4.
    int number = 0;
    char next = '?';

    printf("Un entero: ");
    int count = scanf("%d", &number);
    scanf(" %c", &next);

    printf("scanf devolvió %d\n", count);
    printf("number = %d\n", number);
    printf("Lo siguiente en la entrada es %c\n", next);
    return 0;
}
