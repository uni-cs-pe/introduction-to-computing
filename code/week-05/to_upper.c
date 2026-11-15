#include <stdio.h>

// Copia la entrada y cambia las minúsculas ASCII por mayúsculas.
int main(void) {
    int c = getchar();
    while (c != EOF) {
        if (c >= 'a' && c <= 'z') {
            c = c - 'a' + 'A';
        }
        putchar(c);
        c = getchar();
    }
    return 0;
}
