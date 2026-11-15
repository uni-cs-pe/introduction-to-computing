#include <stdio.h>

// Escribe los días de un mes de un año no bisiesto.
int main(void) {
    int month;
    int days;

    if (scanf("%d", &month) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }

    switch (month) {
        case 4:
        case 6:
        case 9:
        case 11:
            days = 30;
            break;
        case 2:
            days = 28;
            break;
        case 1:
        case 3:
        case 5:
        case 7:
        case 8:
        case 10:
        case 12:
            days = 31;
            break;
        default:
            printf("Mes inválido\n");
            return 1;
    }

    printf("%d días\n", days);
    return 0;
}
