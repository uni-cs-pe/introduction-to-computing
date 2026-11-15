// Un arreglo de cadenas es una matriz de char: cada fila guarda una cadena.
#include <stdio.h>
#include <string.h>

#define COUNT 4
#define NAME_SIZE 12

// Requiere size >= 1. Es la copia segura de safe_copy.c.
void safe_copy(char dest[], const char src[], int size) {
    strncpy(dest, src, size - 1);
    dest[size - 1] = '\0';
}

// Devuelve el índice de la cadena que va primero según strcmp.
int first_name(char names[][NAME_SIZE], int n) {
    int first = 0;
    for (int i = 1; i < n; i++) {
        if (strcmp(names[i], names[first]) < 0) {
            first = i;
        }
    }
    return first;
}

int main(void) {
    char names[COUNT][NAME_SIZE] = {"Rosa", "Ana", "Luis", "Zoila"};

    printf("sizeof(names) = %zu\n", sizeof(names));
    for (int i = 0; i < COUNT; i++) {
        printf("names[%d] = %s, %zu bytes de texto\n", i, names[i], strlen(names[i]));
    }
    printf("Primero: %s\n", names[first_name(names, COUNT)]);

    safe_copy(names[1], "Maria de los Angeles", NAME_SIZE);
    printf("names[1] = %s\n", names[1]);
    printf("Primero: %s\n", names[first_name(names, COUNT)]);
    return 0;
}
