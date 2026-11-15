// Error a propósito: para leer un double, scanf necesita %lf.
#include <stdio.h>

int main(void) {
    double price = 0.0;

    scanf("%f", &price);
    printf("%.2f\n", price);
    return 0;
}
