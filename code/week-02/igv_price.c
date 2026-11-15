// Precio con IGV. La tasa es una constante: el programa no puede cambiarla.
// Aún no revisa lo que devuelve scanf: eso llega con el if, en la semana 4.
#include <stdio.h>

int main(void) {
    const double IGV_RATE = 0.18;
    double price = 0.0;

    printf("Precio sin IGV: ");
    scanf("%lf", &price);

    double igv = price * IGV_RATE;
    double total = price + igv;

    printf("IGV: %.2f\n", igv);
    printf("Total: %.2f\n", total);
    return 0;
}
