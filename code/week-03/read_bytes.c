// Lee 4 bytes y escribe cada uno en hexadecimal. %c lee un byte, no un carácter.
#include <stdio.h>

int main(void) {
    char b0 = 0;
    char b1 = 0;
    char b2 = 0;
    char b3 = 0;
    int read_count = scanf("%c%c%c%c", &b0, &b1, &b2, &b3);
    printf("scanf leyó %d byte(s)\n", read_count);

    // El cast evita que un byte de 128 o más se vea negativo donde char tiene signo.
    printf("%02x %02x %02x %02x\n", (unsigned char) b0, (unsigned char) b1,
           (unsigned char) b2, (unsigned char) b3);
    return 0;
}
