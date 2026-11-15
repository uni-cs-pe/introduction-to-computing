// A propósito: word tiene 4 bytes y ninguno es '\0'. No es una cadena.
#include <stdio.h>

int main(void) {
    char word[4] = "hola";

    printf("%s\n", word);
    return 0;
}
