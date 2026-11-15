#include <stdio.h>

// Lee notas hasta el fin de la entrada y cuenta cuántas aprueban (11 o más).
int main(void) {
    int grade;
    int total = 0;
    int passed = 0;

    int status = scanf("%d", &grade);
    while (status == 1) {
        total++;
        if (grade >= 11) {
            passed++;
        }
        status = scanf("%d", &grade);
    }

    if (status != EOF) {
        printf("Entrada inválida\n");
        return 1;
    }

    printf("Aprobaron %d de %d\n", passed, total);
    return 0;
}
