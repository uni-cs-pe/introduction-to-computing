// Error a propósito: falta el & en scanf.
#include <stdio.h>

int main(void) {
    int grade = 0;

    scanf("%d", grade);
    printf("%d\n", grade);
    return 0;
}
