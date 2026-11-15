#include <stdio.h>

// Convierte un promedio entero de 0 a 20 en una mención.
// La escala es un ejemplo de la clase, no un reglamento.
int main(void) {
    int average;

    if (scanf("%d", &average) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (average < 0 || average > 20) {
        printf("Promedio fuera de rango\n");
    } else if (average >= 17) {
        printf("Excelente\n");
    } else if (average >= 14) {
        printf("Bueno\n");
    } else if (average >= 11) {
        printf("Regular\n");
    } else {
        printf("Insuficiente\n");
    }

    return 0;
}
