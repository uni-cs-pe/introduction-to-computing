// Primero scanf y después fgets: hay que descartar el resto de la línea del número.
#include <stdio.h>

#define SIZE 20

void discard_rest(void) {
    int c = getchar();
    while (c != '\n' && c != EOF) {
        c = getchar();
    }
}

int main(void) {
    int age;
    char name[SIZE];

    if (scanf("%d", &age) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }
    discard_rest();
    if (fgets(name, SIZE, stdin) == NULL) {
        printf("Entrada inválida\n");
        return 1;
    }
    printf("Edad: %d\n", age);
    printf("Nombre: %s", name);
    return 0;
}
