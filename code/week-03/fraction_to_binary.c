// Escribe los primeros 9 bits de la parte fraccionaria de un número entre 0 y 1.
#include <stdio.h>

int main(void) {
    double x = 0.0;
    int read_count = scanf("%lf", &x);
    printf("scanf leyó %d dato(s)\n", read_count);

    // Cada paso duplica x. La parte entera, 0 o 1, es el bit; el cast la obtiene.
    x = x * 2;
    int b1 = (int) x;
    x = x - b1;
    x = x * 2;
    int b2 = (int) x;
    x = x - b2;
    x = x * 2;
    int b3 = (int) x;
    x = x - b3;
    x = x * 2;
    int b4 = (int) x;
    x = x - b4;
    x = x * 2;
    int b5 = (int) x;
    x = x - b5;
    x = x * 2;
    int b6 = (int) x;
    x = x - b6;
    x = x * 2;
    int b7 = (int) x;
    x = x - b7;
    x = x * 2;
    int b8 = (int) x;
    x = x - b8;
    x = x * 2;
    int b9 = (int) x;

    printf("0.%d%d%d%d%d%d%d%d%d...\n", b1, b2, b3, b4, b5, b6, b7, b8, b9);
    return 0;
}
