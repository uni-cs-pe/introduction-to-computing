// Factorial con int. El número viene de la entrada para que UBSan lo vigile al correr.
#include <stdio.h>

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }
    int result = 1;
    for (int i = 2; i <= n; i++) {
        result = result * i;
    }
    printf("%d! = %d\n", n, result);
    return 0;
}
