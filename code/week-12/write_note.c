// El modo "w" crea el archivo, o lo deja vacío si ya existía.
#include <stdio.h>

int main(void) {
    FILE *file = fopen("build/nota.txt", "w");
    if (file == NULL) {
        perror("build/nota.txt");
        return 1;
    }
    fprintf(file, "Nota final: %d\n", 15);
    if (fclose(file) != 0) {
        perror("build/nota.txt");
        return 1;
    }
    return 0;
}
