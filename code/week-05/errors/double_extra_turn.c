#include <stdio.h>

// Error a propósito: se esperaban 10 vueltas, pero con x < 1.0 hay una más.
int main(void) {
    int turns = 0;

    for (double x = 0.0; x < 1.0; x += 0.1) {
        turns++;
    }

    printf("Vueltas: %d\n", turns);
    return 0;
}
