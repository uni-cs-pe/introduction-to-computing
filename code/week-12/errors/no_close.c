// Lo escrito con fprintf puede no estar en el archivo hasta fclose.
#include <stdio.h>

#define LINE_SIZE 64

void look(const char path[]) {
    char line[LINE_SIZE];
    FILE *reader = fopen(path, "r");
    if (reader == NULL) {
        perror(path);
        return;
    }
    if (fgets(line, LINE_SIZE, reader) != NULL) {
        printf("El archivo tiene: %s", line);
    } else {
        printf("El archivo todavía está vacío\n");
    }
    fclose(reader);
}

int main(void) {
    FILE *writer = fopen("build/buffer.txt", "w");
    if (writer == NULL) {
        perror("build/buffer.txt");
        return 1;
    }
    fprintf(writer, "Nota: 15\n");
    look("build/buffer.txt");
    fclose(writer);
    look("build/buffer.txt");
    return 0;
}
