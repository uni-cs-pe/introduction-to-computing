#include <assert.h>
#include <stdio.h>

// Copia de la función de discount.c, porque cada programa está en un solo archivo.
int price_after_discount(int total) {
    if (total >= 10000) {
        return total - total / 10;
    }
    return total;
}

int main(void) {
    assert(price_after_discount(12050) == 10845);   // caso normal con descuento
    assert(price_after_discount(8000) == 8000);     // caso normal sin descuento
    assert(price_after_discount(9999) == 9999);     // último valor sin descuento
    assert(price_after_discount(10000) == 9000);    // primer valor con descuento
    assert(price_after_discount(0) == 0);           // el menor total válido

    printf("Todas las pruebas pasaron\n");
    return 0;
}
