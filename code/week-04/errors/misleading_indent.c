#include <stdio.h>

// Error a propósito: sin llaves, el if solo gobierna una instrucción.
int main(void) {
    int grade;

    if (scanf("%d", &grade) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    if (grade < 0)
        printf("Nota negativa\n");
        printf("Rechazada\n");

    return 0;
}
