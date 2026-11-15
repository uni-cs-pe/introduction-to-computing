// Un char guarda un número: el código del carácter.
#include <stdio.h>

int main(void) {
    char letter = 'A';
    char digit = '7';

    printf("%c tiene el código %d\n", letter, letter);
    printf("%c tiene el código %d\n", letter + 1, letter + 1);
    printf("'a' - 'A' = %d\n", 'a' - 'A');
    printf("minúscula de %c: %c\n", letter, letter + 32);
    printf("%c tiene el código %d\n", digit, digit);
    printf("'7' - '0' = %d\n", digit - '0');
    return 0;
}
