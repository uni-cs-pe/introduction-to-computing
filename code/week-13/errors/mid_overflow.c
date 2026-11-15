// Error a propósito: low + high puede no caber en un int, aunque el resultado sí cabría.
#include <stdio.h>

int main(void) {
    int low;
    int high;
    if (scanf("%d %d", &low, &high) != 2) {
        printf("Entrada inválida\n");
        return 1;
    }
    printf("Fórmula segura: %d\n", low + (high - low) / 2);
    printf("Fórmula con la suma: %d\n", (low + high) / 2);
    return 0;
}
