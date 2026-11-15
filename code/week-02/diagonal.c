// Diagonal de un rectángulo, con el teorema de Pitágoras.
// Aún no revisa lo que devuelve scanf: eso llega con el if, en la semana 4.
#include <math.h>
#include <stdio.h>

int main(void) {
    double width = 0.0;
    double height = 0.0;

    printf("Ancho y alto en metros: ");
    scanf("%lf %lf", &width, &height);

    double diagonal = sqrt(width * width + height * height);

    printf("Diagonal: %.2f metros\n", diagonal);
    return 0;
}
