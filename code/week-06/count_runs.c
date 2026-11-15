#include <stdio.h>

// Lee n y cuenta cuántas veces corre cada línea en dos formas de anidar ciclos.
int main(void) {
    int n;
    int outer_runs = 0;
    int square_runs = 0;
    int triangle_runs = 0;

    if (scanf("%d", &n) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    // Con 5000 como límite, los contadores caben de sobra en un int.
    if (n < 1 || n > 5000) {
        printf("n debe estar entre 1 y 5000\n");
        return 1;
    }

    // El ciclo interior siempre da n vueltas.
    for (int row = 1; row <= n; row++) {
        outer_runs++;
        for (int col = 1; col <= n; col++) {
            square_runs++;
        }
    }

    // El ciclo interior da row vueltas: depende del exterior.
    for (int row = 1; row <= n; row++) {
        for (int col = 1; col <= row; col++) {
            triangle_runs++;
        }
    }

    printf("n = %d\n", n);
    printf("Línea del ciclo exterior: %d\n", outer_runs);
    printf("Línea interior, cuadrado: %d\n", square_runs);
    printf("Línea interior, triángulo: %d\n", triangle_runs);
    return 0;
}
