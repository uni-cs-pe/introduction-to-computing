#include <stdio.h>
#include <stdlib.h>

// Lee una semilla y una cantidad de lanzamientos. Cuenta cuánto salió cada cara.
int main(void) {
    int seed, rolls;
    int one = 0, two = 0, three = 0, four = 0, five = 0, six = 0;

    if (scanf("%d %d", &seed, &rolls) != 2) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (seed < 0) {
        printf("La semilla no puede ser negativa\n");
        return 1;
    }

    if (rolls < 1 || rolls > 10000000) {
        printf("Los lanzamientos deben estar entre 1 y 10000000\n");
        return 1;
    }

    srand((unsigned) seed);

    for (int i = 1; i <= rolls; i++) {
        int die = 1 + rand() % 6;

        switch (die) {
            case 1: one++; break;
            case 2: two++; break;
            case 3: three++; break;
            case 4: four++; break;
            case 5: five++; break;
            default: six++; break;
        }
    }

    printf("Cara 1: %d\n", one);
    printf("Cara 2: %d\n", two);
    printf("Cara 3: %d\n", three);
    printf("Cara 4: %d\n", four);
    printf("Cara 5: %d\n", five);
    printf("Cara 6: %d\n", six);
    return 0;
}
