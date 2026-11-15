// Pide el nombre de un archivo y escribe sus líneas numeradas.
#include <stdio.h>

#define NAME_SIZE 128
#define LINE_SIZE 64

int remove_newline(char s[]) {
    for (int i = 0; s[i] != '\0'; i++) {
        if (s[i] == '\n') {
            s[i] = '\0';
            return 1;
        }
    }
    return 0;
}

int main(void) {
    char path[NAME_SIZE];
    if (fgets(path, NAME_SIZE, stdin) == NULL) {
        printf("Entrada inválida\n");
        return 1;
    }
    remove_newline(path);

    FILE *file = fopen(path, "r");
    if (file == NULL) {
        perror(path);
        return 1;
    }

    char line[LINE_SIZE];
    int number = 0;
    while (fgets(line, LINE_SIZE, file) != NULL) {
        remove_newline(line);
        number++;
        printf("%d: %s\n", number, line);
    }
    fclose(file);

    printf("Total: %d líneas\n", number);
    return 0;
}
