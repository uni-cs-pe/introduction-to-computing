#include <stdio.h>

// Error a propósito: getchar devuelve int, y aquí se guarda en un char.
int main(void) {
    char c;
    int count = 0;

    while ((c = getchar()) != EOF) {
        count++;
    }

    printf("%d bytes\n", count);
    return 0;
}
