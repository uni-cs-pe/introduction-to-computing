#include <stdio.h>

int square(int x) {
    return x * x;
}

// El 2.5 se convierte a int, y se pierde la parte decimal. gcc no avisa.
int main(void) {
    printf("%d\n", square(2.5));
    return 0;
}
