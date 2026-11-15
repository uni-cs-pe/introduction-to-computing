// 0.1 + 0.2 no da exactamente 0.3.
#include <stdio.h>

int main(void) {
    double a = 0.1;
    double b = 0.2;
    double c = 0.3;
    double sum = a + b;

    printf("con %%f:     %f\n", sum);
    printf("0.1       = %.20f\n", a);
    printf("0.2       = %.20f\n", b);
    printf("0.3       = %.20f\n", c);
    printf("0.1 + 0.2 = %.20f\n", sum);
    printf("diferencia = %.20f\n", sum - c);
    // Una comparación vale 1 si es verdadera y 0 si es falsa.
    printf("sum == c vale %d\n", sum == c);
    return 0;
}
