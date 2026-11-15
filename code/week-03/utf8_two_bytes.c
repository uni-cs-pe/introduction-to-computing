// Calcula los dos bytes UTF-8 de un código Unicode de 128 a 2047.
#include <stdio.h>

int main(void) {
    int code = 0;
    int read_count = scanf("%d", &code);
    printf("scanf leyó %d dato(s)\n", read_count);

    // Sin if no podemos rechazar otros códigos: fuera del rango, el resultado no sirve.
    int first = 192 + code / 64;   // 110xxxxx: los 5 bits altos
    int second = 128 + code % 64;  // 10xxxxxx: los 6 bits bajos

    printf("bytes: %x %x\n", first, second);
    printf("carácter: %c%c\n", first, second);
    return 0;
}
