#include <stdio.h>

#define DAYS 7

// Suma, promedio y mayor de las temperaturas de una semana.
int main(void) {
    int temperatures[DAYS] = {-2, 1, 4, -5, 0, 3, 2};
    int sum = 0;

    for (int i = 0; i < DAYS; i++) {
        sum = sum + temperatures[i];
    }

    int max_day = 0;
    for (int i = 1; i < DAYS; i++) {
        if (temperatures[i] > temperatures[max_day]) {
            max_day = i;
        }
    }

    printf("Suma: %d\n", sum);
    printf("Promedio: %.2f\n", (double) sum / DAYS);
    printf("Mayor: %d, en el día %d\n", temperatures[max_day], max_day);
    return 0;
}
