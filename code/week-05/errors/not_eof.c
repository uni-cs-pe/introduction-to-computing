#include <stdio.h>

// Error a propósito: != EOF deja pasar el 0 que devuelve scanf ante un dato inválido.
int main(void) {
    int n = 0;
    int count = 0;

    while (scanf("%d", &n) != EOF) {
        count++;
        printf("Llevo %d datos; el último es %d\n", count, n);
    }

    return 0;
}
