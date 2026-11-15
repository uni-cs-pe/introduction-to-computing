// Escribe en binario un número de 0 a 255, con divisiones sucesivas entre 2.
#include <stdio.h>

int main(void) {
    int n = 0;
    // Mostramos cuántos datos leyó scanf. Con if, la próxima semana, ya podremos reaccionar.
    int read_count = scanf("%d", &n);
    printf("scanf leyó %d dato(s)\n", read_count);

    int b0 = n % 2;
    n = n / 2;
    int b1 = n % 2;
    n = n / 2;
    int b2 = n % 2;
    n = n / 2;
    int b3 = n % 2;
    n = n / 2;
    int b4 = n % 2;
    n = n / 2;
    int b5 = n % 2;
    n = n / 2;
    int b6 = n % 2;
    n = n / 2;
    int b7 = n % 2;

    // El primer resto es el bit de menor peso: se escribe al final.
    printf("%d%d%d%d%d%d%d%d\n", b7, b6, b5, b4, b3, b2, b1, b0);
    return 0;
}
