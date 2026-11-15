// Error: strcat no recibe el tamaño del destino. Compila sin advertencias.
#include <stdio.h>
#include <string.h>

int main(void) {
    char word[20];
    char full[8] = "Ana ";

    if (scanf("%19s", word) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }
    strcat(full, word);
    printf("%s\n", full);
    return 0;
}
