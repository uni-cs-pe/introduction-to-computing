// Lee dos líneas con fgets. Quita el salto de línea y descarta lo que no cupo.
#include <stdio.h>

#define SIZE 20

// Si la cadena tiene '\n', lo quita y devuelve 1. Si no, devuelve 0.
int remove_newline(char s[]) {
    for (int i = 0; s[i] != '\0'; i++) {
        if (s[i] == '\n') {
            s[i] = '\0';
            return 1;
        }
    }
    return 0;
}

// Lee y descarta lo que queda de la línea actual.
void discard_rest(void) {
    int c = getchar();
    while (c != '\n' && c != EOF) {
        c = getchar();
    }
}

// Lee una línea en s. Devuelve 0 si la entrada ya terminó y 1 si leyó algo.
int read_text(char s[], int size) {
    if (fgets(s, size, stdin) == NULL) {
        return 0;
    }
    if (!remove_newline(s)) {
        discard_rest();
    }
    return 1;
}

int main(void) {
    char name[SIZE];
    char city[SIZE];

    if (!read_text(name, SIZE) || !read_text(city, SIZE)) {
        printf("Entrada inválida\n");
        return 1;
    }
    printf("Nombre: %s\n", name);
    printf("Ciudad: %s\n", city);
    return 0;
}
