#include <stdio.h>

// Error a propósito: no revisa scanf. Con abc, el dato nunca se consume.
int main(void) {
    int month = 0;

    do {
        scanf("%d", &month);
        printf("Mes fuera de rango\n");
    } while (month < 1 || month > 12);

    printf("Mes elegido: %d\n", month);
    return 0;
}
