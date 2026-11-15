// Copia una cadena sin pasarse: quien escribe en un arreglo recibe su tamaño.
#include <stdio.h>

#define SIZE 5

// Requiere size >= 1. Copia como máximo size - 1 bytes y siempre termina en '\0'.
void copy_text(char dest[], const char src[], int size) {
    int i = 0;
    while (src[i] != '\0' && i < size - 1) {
        dest[i] = src[i];
        i++;
    }
    dest[i] = '\0';
}

int main(void) {
    char word[SIZE];

    copy_text(word, "sol", SIZE);
    printf("%s\n", word);
    copy_text(word, "luna", SIZE);
    printf("%s\n", word);
    copy_text(word, "estrella", SIZE);
    printf("%s\n", word);
    return 0;
}
