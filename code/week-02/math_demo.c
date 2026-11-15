// Funciones de math.h. Reciben y devuelven double. Se compila con -lm.
// Aún no revisa lo que devuelve scanf: eso llega con el if, en la semana 4.
#include <math.h>
#include <stdio.h>

int main(void) {
    double x = 0.0;

    printf("x: ");
    scanf("%lf", &x);

    printf("sqrt(x)   = %f\n", sqrt(x));
    printf("pow(x, 3) = %f\n", pow(x, 3));
    printf("fabs(x)   = %f\n", fabs(x));
    printf("floor(x)  = %f\n", floor(x));
    printf("ceil(x)   = %f\n", ceil(x));
    printf("round(x)  = %f\n", round(x));
    return 0;
}
