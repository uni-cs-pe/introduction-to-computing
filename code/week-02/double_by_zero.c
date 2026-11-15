// Con double, dividir entre cero no detiene el programa: da inf.
// Aún no revisa lo que devuelve scanf: eso llega con el if, en la semana 4.
#include <stdio.h>

int main(void) {
    double a = 0.0;
    double b = 0.0;

    printf("Dos números: ");
    scanf("%lf %lf", &a, &b);

    printf("Cociente: %f\n", a / b);
    return 0;
}
