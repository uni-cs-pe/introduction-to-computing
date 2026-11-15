// Lo que strncpy deja en el destino: a veces sin '\0', a veces con muchos.
#include <stdio.h>
#include <string.h>

#define SIZE 5

// Escribe los bytes como números. No usa %s: el arreglo puede no ser una cadena.
void print_bytes(const char a[], int size) {
    for (int i = 0; i < size; i++) {
        printf(" %d", a[i]);
    }
    printf("\n");
}

void fill(char dest[], const char src[]) {
    strncpy(dest, src, SIZE);
}

int main(void) {
    char word[SIZE];

    fill(word, "sol");
    print_bytes(word, SIZE);
    fill(word, "luna");
    print_bytes(word, SIZE);
    fill(word, "estrella");
    print_bytes(word, SIZE);
    return 0;
}
