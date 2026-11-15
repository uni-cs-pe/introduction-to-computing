// scanf devuelve cuántos datos pudo guardar. Aquí solo lo mostramos:
// actuar según ese número necesita el if de la semana 4.
#include <stdio.h>

int main(void) {
    int first = 0;
    int second = 0;

    printf("Dos enteros: ");
    int count = scanf("%d %d", &first, &second);

    printf("scanf devolvió %d\n", count);
    printf("first = %d, second = %d\n", first, second);
    return 0;
}
