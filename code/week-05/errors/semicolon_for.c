#include <stdio.h>

// Error a propósito: el ; termina el for, que queda sin cuerpo.
int main(void) {
    int i;

    for (i = 1; i <= 3; i++);
    {
        printf("%d\n", i);
    }

    return 0;
}
