// Cuántos bytes ocupa cada tipo. sizeof da un resultado que se escribe con %zu.
#include <stdio.h>

int main(void) {
    int age = 19;

    printf("int: %zu bytes\n", sizeof(int));
    printf("double: %zu bytes\n", sizeof(double));
    printf("char: %zu bytes\n", sizeof(char));
    printf("la variable age: %zu bytes\n", sizeof(age));
    printf("age vale %d\n", age);
    return 0;
}
