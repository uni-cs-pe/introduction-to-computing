#include <stdio.h>

// Error a propósito: 'a' es un carácter, "a" es otra cosa, una cadena.
int main(void) {
    char letter = 'a';

    if (letter == "a") {
        printf("Es la letra a\n");
    }

    return 0;
}
