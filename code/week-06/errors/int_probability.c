#include <stdio.h>
#include <stdlib.h>

// ERROR: hits / trials es una división entera.
int main(void) {
    int trials = 1000000;
    int hits = 0;

    srand(42);

    for (int i = 1; i <= trials; i++) {
        int d1 = 1 + rand() % 6;
        int d2 = 1 + rand() % 6;

        if (d1 + d2 == 7) {
            hits++;
        }
    }

    double estimate = hits / trials;
    printf("Estimación: %.4f\n", estimate);
    return 0;
}
