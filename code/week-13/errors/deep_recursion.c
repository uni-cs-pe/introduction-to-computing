// Tiene caso base, pero con un n muy grande la pila no alcanza.
#include <stdio.h>

long long sum_down(int n) {
    if (n <= 0) {
        return 0;
    }
    return n + sum_down(n - 1);
}

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }
    printf("%lld\n", sum_down(n));
    return 0;
}
