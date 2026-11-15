// Los formatos de printf. Cada % se reemplaza por un valor, en orden.
#include <stdio.h>

int main(void) {
    int grade = 15;
    double height = 1.685;
    char section = 'B';

    printf("Nota: %d\n", grade);
    printf("Estatura: %f\n", height);
    printf("Estatura: %.2f\n", height);
    printf("Sección: %c\n", section);
    printf("Nota %d, sección %c\n", grade, section);
    printf("Avance: %d%%\n", 80);
    printf("Columna 1\tColumna 2\n");
    printf("2.675 con dos decimales: %.2f\n", 2.675);
    return 0;
}
