#include <stdio.h>

// Cambia su copia de x. El x de main no se entera.
void add_one(int x) {
    x = x + 1;
    printf("En add_one, x vale %d\n", x);
}

// Devuelve el nuevo valor: quien llama decide qué hacer con él.
int plus_one(int x) {
    return x + 1;
}

int main(void) {
    int x = 1;

    add_one(x);
    printf("En main, x vale %d\n", x);

    x = plus_one(x);
    printf("Después de plus_one, x vale %d\n", x);
    return 0;
}
