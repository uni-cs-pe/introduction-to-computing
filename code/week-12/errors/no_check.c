// Error: no se revisa el resultado de fopen, y el archivo no existe.
#include <stdio.h>

#define LINE_SIZE 64

int main(void) {
    FILE *file = fopen("no_existe.txt", "r");
    char line[LINE_SIZE];

    while (fgets(line, LINE_SIZE, file) != NULL) {
        printf("%s", line);
    }
    fclose(file);
    return 0;
}
