#include <stdio.h>

// Error a propósito: switch solo trabaja con enteros, y char es un entero.
int main(void) {
    double grade = 10.5;

    switch (grade) {
        case 10:
            printf("Diez\n");
            break;
        default:
            printf("Otra\n");
    }

    return 0;
}
