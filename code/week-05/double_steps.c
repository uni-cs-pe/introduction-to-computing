#include <stdio.h>

// Cuenta con un entero y calcula el double en cada vuelta: siempre son 11 valores.
int main(void) {
    for (int i = 0; i <= 10; i++) {
        double x = i / 10.0;
        printf("%.1f\n", x);
    }

    return 0;
}
