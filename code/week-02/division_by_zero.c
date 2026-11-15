// Dividir enteros entre cero es un error de ejecución.
// Aún no revisa lo que devuelve scanf: eso llega con el if, en la semana 4.
#include <stdio.h>

int main(void) {
    int a = 0;
    int b = 0;

    printf("Dos enteros: ");
    scanf("%d %d", &a, &b);

    int quotient = a / b;

    printf("Cociente: %d\n", quotient);
    return 0;
}
