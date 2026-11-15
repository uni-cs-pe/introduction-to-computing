// Cuenta los primos hasta un límite que lee de la entrada.
#include <stdio.h>

int is_prime(int n) {
    if (n < 2) {
        return 0;
    }
    int d = 2;
    while (d <= n / d) {
        if (n % d == 0) {
            return 0;
        }
        d = d + 1;
    }
    return 1;
}

int main(void) {
    int limit;
    if (scanf("%d", &limit) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }
    int count = 0;
    for (int n = 2; n <= limit; n++) {
        if (is_prime(n)) {
            count = count + 1;
        }
    }
    printf("Hay %d primos hasta %d\n", count, limit);
    return 0;
}
