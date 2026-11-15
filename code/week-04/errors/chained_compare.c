#include <stdio.h>

// Error a propósito: en C, 0 <= grade <= 20 no significa lo que parece.
int main(void) {
    int grade;

    if (scanf("%d", &grade) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (0 <= grade <= 20) {
        printf("En rango\n");
    } else {
        printf("Fuera de rango\n");
    }

    return 0;
}
