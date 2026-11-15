// Recorre una cadena y cuenta las minúsculas. Funciona solo para ASCII.
#include <stdio.h>

int count_lowercase(const char s[]) {
    int count = 0;
    for (int i = 0; s[i] != '\0'; i++) {
        if (s[i] >= 'a' && s[i] <= 'z') {
            count++;
        }
    }
    return count;
}

int main(void) {
    printf("Hola Mundo: %d\n", count_lowercase("Hola Mundo"));
    printf("LIMA 2026: %d\n", count_lowercase("LIMA 2026"));
    printf("ano: %d\n", count_lowercase("ano"));
    printf("año: %d\n", count_lowercase("año"));
    return 0;
}
