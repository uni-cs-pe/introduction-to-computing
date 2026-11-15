#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Devuelve el resultado de lanzar un dado: un entero de 1 a 6.
int roll_die(void) {
    return 1 + rand() % 6;
}

int main(void) {
    srand((unsigned) time(NULL));

    for (int i = 0; i < 5; i++) {
        printf("%d ", roll_die());
    }
    printf("\n");
    return 0;
}
