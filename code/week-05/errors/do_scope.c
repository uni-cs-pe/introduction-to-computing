#include <stdio.h>

// Error a propósito: month nace dentro del bloque y la condición está afuera.
int main(void) {
    do {
        int month;
        if (scanf("%d", &month) != 1) {
            return 1;
        }
    } while (month < 1 || month > 12);

    return 0;
}
