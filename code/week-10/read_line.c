// Muestra qué deja fgets en el buffer en cada lectura.
#include <stdio.h>

#define SIZE 8

// Escribe la cadena con \n visible, para ver si el salto de línea está.
void print_visible(const char s[]) {
    for (int i = 0; s[i] != '\0'; i++) {
        if (s[i] == '\n') {
            printf("\\n");
        } else {
            printf("%c", s[i]);
        }
    }
}

int main(void) {
    char line[SIZE];

    while (fgets(line, SIZE, stdin) != NULL) {
        printf("leído: \"");
        print_visible(line);
        printf("\"\n");
    }
    printf("fgets devolvió NULL\n");
    return 0;
}
