// Error a propósito: la ñ no cabe en un char.
#include <stdio.h>

int main(void) {
    char letter = 'ñ';

    printf("%c\n", letter);
    return 0;
}
