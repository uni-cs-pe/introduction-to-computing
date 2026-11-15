// Un char guarda un número pequeño, el código de un carácter.
#include <stdio.h>

int main(void) {
    char letter = 'A';
    char digit = '7';

    printf("%c tiene el código %d\n", letter, letter);
    printf("La letra siguiente es %c\n", letter + 1);
    printf("%c tiene el código %d\n", digit, digit);
    printf("El valor numérico de %c es %d\n", digit, digit - '0');
    return 0;
}
