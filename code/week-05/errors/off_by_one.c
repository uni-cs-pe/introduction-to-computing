#include <stdio.h>

// Error a propósito: quería escribir del 1 al 5, pero la condición corta antes.
int main(void) {
    for (int i = 1; i < 5; i++) {
        printf("%d\n", i);
    }

    return 0;
}
