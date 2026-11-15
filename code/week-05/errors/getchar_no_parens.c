#include <stdio.h>

// Error a propósito: sin paréntesis, c recibe el resultado de la comparación.
int main(void) {
    int c;
    int newlines = 0;

    while (c = getchar() != EOF) {
        if (c == '\n') {
            newlines++;
        }
    }

    printf("%d saltos de línea\n", newlines);
    return 0;
}
