#include <stdio.h>

// Error: si la nota es menor que 11, la función termina sin return.
int is_passing(int grade) {
    if (grade >= 11) {
        return 1;
    }
}

int main(void) {
    int grade;

    if (scanf("%d", &grade) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    printf("%d\n", is_passing(grade));
    return 0;
}
