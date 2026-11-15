#include <assert.h>
#include <stdio.h>

// Devuelve cuántas cifras tiene n. El 0 tiene una cifra; el signo no cuenta.
int count_digits(int n) {
    if (n == 0) {
        return 1;
    }

    int count = 0;
    while (n != 0) {
        count = count + 1;
        n = n / 10;
    }
    return count;
}

int main(void) {
    assert(count_digits(7) == 1);
    assert(count_digits(2026) == 4);
    assert(count_digits(0) == 1);
    assert(count_digits(-42) == 2);
    assert(count_digits(10) == 2);
    assert(count_digits(9) == 1);

    printf("Todas las pruebas pasaron\n");
    return 0;
}
