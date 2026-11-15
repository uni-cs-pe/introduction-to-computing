// Copiar con strncpy sin perder el '\0': se copia size - 1 y se pone a mano.
#include <stdio.h>
#include <string.h>

#define SIZE 5

// Requiere size >= 1. Da el mismo texto que copy_text; además, strncpy rellena lo que sobra.
void safe_copy(char dest[], const char src[], int size) {
    strncpy(dest, src, size - 1);
    dest[size - 1] = '\0';
}

int main(void) {
    char word[SIZE];

    safe_copy(word, "sol", SIZE);
    printf("%s\n", word);
    safe_copy(word, "luna", SIZE);
    printf("%s\n", word);
    safe_copy(word, "estrella", SIZE);
    printf("%s\n", word);
    return 0;
}
