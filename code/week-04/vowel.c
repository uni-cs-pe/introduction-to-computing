#include <stdio.h>

// Dice si un carácter es una vocal sin tilde.
int main(void) {
    char letter;

    if (scanf(" %c", &letter) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    switch (letter) {
        case 'a':
        case 'e':
        case 'i':
        case 'o':
        case 'u':
        case 'A':
        case 'E':
        case 'I':
        case 'O':
        case 'U':
            printf("Vocal\n");
            break;
        default:
            printf("No es vocal\n");
    }

    return 0;
}
