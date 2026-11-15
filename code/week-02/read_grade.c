// Primer programa que lee un dato del teclado.
#include <stdio.h>

int main(void) {
    int grade = 0;

    printf("Nota: ");
    scanf("%d", &grade);    // aún no revisamos lo que devuelve: ver read_check.c
    printf("Leí la nota %d\n", grade);
    printf("Con dos puntos más sería %d\n", grade + 2);
    return 0;
}
