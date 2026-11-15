#include <stdio.h>

// Error a propósito: ! se aplica antes que ==, solo a la variable a.
int main(void) {
    int a = 5;
    int b = 3;

    if (!a == b) {
        printf("a es distinto de b\n");
    } else {
        printf("a es igual a b\n");
    }

    return 0;
}
