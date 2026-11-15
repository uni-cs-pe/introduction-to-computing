#include <stdio.h>

// Error de lógica: decide con la primera cifra, sin mirar las demás.
int has_digit(int n, int digit) {
    while (n > 0) {
        if (n % 10 == digit) {
            return 1;
        } else {
            return 0;
        }
        n = n / 10;
    }
    return 0;
}

int main(void) {
    int n, digit;

    if (scanf("%d %d", &n, &digit) != 2 || n <= 0) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (has_digit(n, digit)) {
        printf("Sí aparece\n");
    } else {
        printf("No aparece\n");
    }
    return 0;
}
