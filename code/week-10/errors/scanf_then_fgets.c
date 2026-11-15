// A propósito: scanf deja el salto de línea y fgets lo lee como una línea vacía.
#include <stdio.h>

#define SIZE 20

int main(void) {
    int age;
    char name[SIZE];

    if (scanf("%d", &age) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }
    if (fgets(name, SIZE, stdin) == NULL) {
        printf("Entrada inválida\n");
        return 1;
    }
    printf("Edad: %d\n", age);
    printf("Nombre: %s", name);
    return 0;
}
