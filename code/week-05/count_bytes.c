#include <stdio.h>

// Cuenta los bytes de la entrada, hasta EOF.
int main(void) {
    int count = 0;

    int c = getchar();
    while (c != EOF) {
        count++;
        c = getchar();
    }

    printf("%d bytes\n", count);
    return 0;
}
