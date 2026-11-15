// Error: feof como condición del ciclo. La última línea sale dos veces.
#include <stdio.h>

#define LINE_SIZE 64

int main(void) {
    FILE *file = fopen("compras.txt", "r");
    if (file == NULL) {
        perror("compras.txt");
        return 1;
    }

    char line[LINE_SIZE];
    while (!feof(file)) {
        fgets(line, LINE_SIZE, file);
        printf("%s", line);
    }
    fclose(file);
    return 0;
}
