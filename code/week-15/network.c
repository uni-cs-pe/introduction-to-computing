// Tres neuronas en dos capas, con pesos escritos a mano, calculan XOR.
// Una sola neurona no puede: el programa prueba todos los pesos enteros de -3 a 3.
#include <stdio.h>

#define LIMIT 3

struct neuron {
    int w_a;
    int w_b;
    int base;
};

int fire(struct neuron n, int a, int b) {
    return n.w_a * a + n.w_b * b + n.base > 0;
}

// Devuelve 1 si la neurona da XOR en los cuatro casos.
int computes_xor(struct neuron n) {
    for (int a = 0; a <= 1; a++) {
        for (int b = 0; b <= 1; b++) {
            if (fire(n, a, b) != (a != b)) {
                return 0;
            }
        }
    }
    return 1;
}

int main(void) {
    struct neuron n_or = {1, 1, 0};
    struct neuron n_nand = {-1, -1, 2};
    struct neuron n_and = {1, 1, -1};

    printf("a b  or nand  salida\n");
    for (int a = 0; a <= 1; a++) {
        for (int b = 0; b <= 1; b++) {
            int first = fire(n_or, a, b);
            int second = fire(n_nand, a, b);
            printf("%d %d  %2d %4d  %6d\n", a, b, first, second, fire(n_and, first, second));
        }
    }

    int tried = 0;
    int found = 0;
    for (int w_a = -LIMIT; w_a <= LIMIT; w_a++) {
        for (int w_b = -LIMIT; w_b <= LIMIT; w_b++) {
            for (int base = -LIMIT; base <= LIMIT; base++) {
                struct neuron n = {w_a, w_b, base};
                tried++;
                found = found + computes_xor(n);
            }
        }
    }
    printf("Una sola neurona: %d de %d combinaciones de pesos dan XOR\n", found, tried);
    return 0;
}
