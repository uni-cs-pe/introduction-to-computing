// El mismo cálculo de dinero en soles con double y en céntimos con int.
#include <stdio.h>

int main(void) {
    double price = 1.10;
    double total = price * 3;
    printf("3 x 1.10 con double: %.20f\n", total);
    printf("lo mismo con %%.2f:   %.2f\n", total);

    double balance = 1.00 - 0.10 - 0.10 - 0.10 - 0.10 - 0.10 - 0.10 - 0.10 - 0.10 - 0.10 - 0.10;
    printf("saldo con double:    %.20f\n", balance);

    int price_cents = 110;
    int total_cents = price_cents * 3;
    printf("3 x 110 céntimos:    %d\n", total_cents);
    printf("en soles:            S/ %d.%02d\n", total_cents / 100, total_cents % 100);

    int balance_cents = 100 - 10 - 10 - 10 - 10 - 10 - 10 - 10 - 10 - 10 - 10;
    printf("saldo en céntimos:   %d\n", balance_cents);
    return 0;
}
