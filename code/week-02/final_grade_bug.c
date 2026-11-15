// Tiene un error a propósito: compila sin avisos, pero divide entre enteros.
// Aún no revisa lo que devuelve scanf: eso llega con el if, en la semana 4.
#include <stdio.h>

int main(void) {
    int ep = 0;
    int ef = 0;
    int pp = 0;

    printf("Examen parcial: ");
    scanf("%d", &ep);
    printf("Examen final: ");
    scanf("%d", &ef);
    printf("Promedio de prácticas: ");
    scanf("%d", &pp);

    double final_grade = (ep + 2 * ef + pp) / 4;

    printf("Promedio final: %.2f\n", final_grade);
    return 0;
}
