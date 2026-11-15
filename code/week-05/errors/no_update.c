#include <stdio.h>

// Error a propósito: nada cambia n dentro del ciclo.
int main(void) {
    int n = 3;

    while (n > 0) {
        printf("%d\n", n);
    }

    return 0;
}
