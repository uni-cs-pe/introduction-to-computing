#include <stdio.h>

// Error a propósito: x nunca vale exactamente 1.0, así que el ciclo no termina.
int main(void) {
    for (double x = 0.0; x != 1.0; x += 0.1) {
        printf("%.17f\n", x);
    }

    return 0;
}
