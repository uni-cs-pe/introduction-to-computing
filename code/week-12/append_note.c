// El modo "a" agrega al final, sin borrar lo que ya hay.
#include <stdio.h>

int main(void) {
    FILE *file = fopen("build/nota.txt", "a");
    if (file == NULL) {
        perror("build/nota.txt");
        return 1;
    }
    fprintf(file, "Otra línea\n");
    if (fclose(file) != 0) {
        perror("build/nota.txt");
        return 1;
    }
    return 0;
}
