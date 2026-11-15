#include <assert.h>
#include <stdio.h>

// Debería devolver cuántas cifras tiene n. Tiene un bug.
int count_digits(int n) {
    int count = 0;
    while (n > 0) {
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

    printf("Todas las pruebas pasaron\n");
    return 0;
}
