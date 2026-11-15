#include <stdio.h>

// Suma precios en céntimos hasta que llegue un 0, que marca el final.
int main(void) {
    int price;
    int total = 0;
    int items = 0;

    int status = scanf("%d", &price);
    while (status == 1 && price != 0) {
        total += price;
        items++;
        status = scanf("%d", &price);
    }

    if (status != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    printf("%d productos: %d.%02d soles\n", items, total / 100, total % 100);
    return 0;
}
