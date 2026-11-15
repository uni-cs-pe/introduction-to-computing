// Dividir entre cero: gcc avisa, pero igual crea el ejecutable.
#include <stdio.h>

int main(void) {
    printf("Antes de dividir\n");
    printf("%d\n", 10 / 0);
    printf("Después de dividir\n");
    return 0;
}
