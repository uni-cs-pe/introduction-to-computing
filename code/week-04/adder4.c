#include <stdio.h>

// Suma dos números de 4 bits con cuatro sumadores de un bit en cadena.
// Sin ciclos, la misma cuenta se repite para cada columna.
int main(void) {
    int a3, a2, a1, a0;
    int b3, b2, b1, b0;

    // %1d lee un solo dígito, así que 0101 se lee como cuatro números.
    if (scanf("%1d%1d%1d%1d %1d%1d%1d%1d",
              &a3, &a2, &a1, &a0, &b3, &b2, &b1, &b0) != 8) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (a3 > 1 || a2 > 1 || a1 > 1 || a0 > 1 ||
        b3 > 1 || b2 > 1 || b1 > 1 || b0 > 1) {
        printf("Los bits deben ser 0 o 1\n");
        return 1;
    }

    int carry0 = 0;

    int partial0 = a0 != b0;
    int sum0 = partial0 != carry0;
    int carry1 = (a0 && b0) || (partial0 && carry0);

    int partial1 = a1 != b1;
    int sum1 = partial1 != carry1;
    int carry2 = (a1 && b1) || (partial1 && carry1);

    int partial2 = a2 != b2;
    int sum2 = partial2 != carry2;
    int carry3 = (a2 && b2) || (partial2 && carry2);

    int partial3 = a3 != b3;
    int sum3 = partial3 != carry3;
    int carry4 = (a3 && b3) || (partial3 && carry3);

    printf("acarreos: %d %d %d %d\n", carry4, carry3, carry2, carry1);
    printf("suma:     %d%d%d%d\n", sum3, sum2, sum1, sum0);
    return 0;
}
