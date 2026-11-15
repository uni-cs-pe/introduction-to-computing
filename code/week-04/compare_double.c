#include <math.h>
#include <stdio.h>

// Dos double casi nunca se comparan con ==. Se pregunta si están muy cerca.
int main(void) {
    double sum = 0.1 + 0.2;

    if (sum == 0.3) {
        printf("Con ==: iguales\n");
    } else {
        printf("Con ==: distintos\n");
    }

    if (fabs(sum - 0.3) < 0.000001) {
        printf("Con tolerancia: iguales\n");
    } else {
        printf("Con tolerancia: distintos\n");
    }

    return 0;
}
