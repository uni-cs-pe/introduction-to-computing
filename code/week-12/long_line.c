// Lee un archivo con un buffer pequeño y distingue las líneas que no caben.
#include <stdio.h>

#define LINE_SIZE 16
#define READ_END 0
#define READ_OK 1
#define READ_TOO_LONG 2

int remove_newline(char s[]) {
    for (int i = 0; s[i] != '\0'; i++) {
        if (s[i] == '\n') {
            s[i] = '\0';
            return 1;
        }
    }
    return 0;
}

int read_line(FILE *file, char line[], int size) {
    if (fgets(line, size, file) == NULL) {
        return READ_END;
    }
    if (remove_newline(line)) {
        return READ_OK;
    }
    int c = fgetc(file);
    if (c == '\n' || c == EOF) {
        return READ_OK;
    }
    while (c != '\n' && c != EOF) {
        c = fgetc(file);
    }
    return READ_TOO_LONG;
}

int main(void) {
    FILE *file = fopen("largas.txt", "r");
    if (file == NULL) {
        perror("largas.txt");
        return 1;
    }

    char line[LINE_SIZE];
    int number = 0;
    int result = read_line(file, line, LINE_SIZE);
    while (result != READ_END) {
        number++;
        if (result == READ_OK) {
            printf("Línea %d: \"%s\"\n", number, line);
        } else {
            printf("Línea %d: no cabe en %d bytes, se descarta\n", number, LINE_SIZE);
        }
        result = read_line(file, line, LINE_SIZE);
    }
    fclose(file);
    return 0;
}
