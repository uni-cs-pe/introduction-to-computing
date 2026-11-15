// Error a propósito: la ñ no cabe en un char. No forma parte de make.
#include <stdio.h>

int main(void) {
    char c = 'ñ';
    printf("%c\n", c);
    return 0;
}
