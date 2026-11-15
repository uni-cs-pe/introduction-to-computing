#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Toma la semilla de la hora actual y lanza un dado diez veces.
int main(void) {
    srand((unsigned) time(NULL));

    for (int i = 1; i <= 10; i++) {
        printf("%d ", 1 + rand() % 6);
    }
    printf("\n");
    return 0;
}
