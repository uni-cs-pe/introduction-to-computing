#include <stdio.h>

// Sumador de un bit: suma a, b y el acarreo que llega.
int main(void) {
    int a, b, carry_in;

    if (scanf("%d %d %d", &a, &b, &carry_in) != 3) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (a < 0 || a > 1 || b < 0 || b > 1 || carry_in < 0 || carry_in > 1) {
        printf("Los bits deben ser 0 o 1\n");
        return 1;
    }

    int partial = a != b;
    int sum = partial != carry_in;
    int carry_out = (a && b) || (partial && carry_in);

    printf("suma %d, acarreo %d\n", sum, carry_out);
    return 0;
}
