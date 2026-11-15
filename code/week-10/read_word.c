// %19s lee una palabra de 19 bytes como máximo: deja lugar para el '\0'.
#include <stdio.h>

int main(void) {
    char word[20];

    if (scanf("%19s", word) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }
    printf("Primera lectura: %s\n", word);

    if (scanf("%19s", word) != 1) {
        printf("No hay más palabras\n");
        return 0;
    }
    printf("Segunda lectura: %s\n", word);
    return 0;
}
