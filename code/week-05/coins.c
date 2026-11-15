#include <stdio.h>

// Cuenta cuántas monedas de S/ 5 caben en un vuelto dado en céntimos.
int main(void) {
    int change;
    int coins = 0;

    if (scanf("%d", &change) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    while (change >= 500) {
        change = change - 500;
        coins = coins + 1;
    }

    printf("%d monedas de S/ 5; quedan %d céntimos\n", coins, change);
    return 0;
}
