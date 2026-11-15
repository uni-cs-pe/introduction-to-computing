#include <stdio.h>

// Devuelve la suma de las cifras de n, que no es negativo.
int digit_sum(int n) {
    int sum = 0;
    while (n > 0) {
        int last = n % 10;
        sum = sum + last;
        n = n / 10;
    }
    return sum;
}

int main(void) {
    int n;

    if (scanf("%d", &n) != 1 || n < 0) {
        printf("Entrada inválida\n");
        return 1;
    }

    int result = digit_sum(n);
    printf("La suma de las cifras de %d es %d\n", n, result);
    return 0;
}
