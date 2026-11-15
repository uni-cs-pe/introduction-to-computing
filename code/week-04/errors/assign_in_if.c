#include <stdio.h>

// Error a propósito: = asigna, == compara.
int main(void) {
    int x = 5;

    if (x = 0) {
        printf("cero\n");
    } else {
        printf("otro\n");
    }
    printf("x vale %d\n", x);

    return 0;
}
