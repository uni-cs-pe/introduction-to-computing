// Interés compuesto: final = capital * (1 + tasa / 100) elevado a años.
// Aún no revisa lo que devuelve scanf: eso llega con el if, en la semana 4.
#include <math.h>
#include <stdio.h>

int main(void) {
    double capital = 0.0;
    double rate = 0.0;
    int years = 0;

    printf("Capital en soles: ");
    scanf("%lf", &capital);
    printf("Tasa anual en %%: ");
    scanf("%lf", &rate);
    printf("Años: ");
    scanf("%d", &years);

    double final_amount = capital * pow(1 + rate / 100, years);

    printf("Monto final: %.2f soles\n", final_amount);
    return 0;
}
