// Un caso exacto y dos límites de double: los errores se acumulan y la precisión se acaba.
#include <stdio.h>

int main(void) {
    double half = 0.5;
    double quarter = 0.25;
    printf("0.5 + 0.25     = %.20f\n", half + quarter);

    double tenths = 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1;
    printf("diez veces 0.1 = %.20f\n", tenths);

    double big = 9007199254740992.0;  // 2 elevado a 53
    double bigger = big + 1.0;
    printf("big            = %.1f\n", big);
    printf("big + 1        = %.1f\n", bigger);
    return 0;
}
