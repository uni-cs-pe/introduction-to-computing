// Muestra el patrón de bits de un entero de -128 a 127, en complemento a dos.
#include <stdio.h>

int main(void) {
    int x = 0;
    int read_count = scanf("%d", &x);
    printf("scanf leyó %d dato(s)\n", read_count);

    // Sin if: si x es negativo da x + 256; si no, da x. Solo vale de -128 a 127.
    int pattern = (x + 256) % 256;

    printf("%d en 8 bits: %d%d%d%d%d%d%d%d\n", x,
           pattern / 128 % 2, pattern / 64 % 2, pattern / 32 % 2, pattern / 16 % 2,
           pattern / 8 % 2, pattern / 4 % 2, pattern / 2 % 2, pattern % 2);
    // %x espera un valor sin signo: por eso el cast. Es el int completo, de 32 bits.
    printf("%d en un int: %08x\n", x, (unsigned int) x);
    return 0;
}
