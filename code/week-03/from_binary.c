// Lee 8 dígitos binarios y escribe el número en decimal y en hexadecimal.
#include <stdio.h>

int main(void) {
    int value = 0;
    int bit = 0;
    int read_count = 0;

    // %1d lee un solo dígito. scanf devuelve 1 cada vez que lo logra.
    read_count = read_count + scanf("%1d", &bit);
    value = value * 2 + bit;
    read_count = read_count + scanf("%1d", &bit);
    value = value * 2 + bit;
    read_count = read_count + scanf("%1d", &bit);
    value = value * 2 + bit;
    read_count = read_count + scanf("%1d", &bit);
    value = value * 2 + bit;
    read_count = read_count + scanf("%1d", &bit);
    value = value * 2 + bit;
    read_count = read_count + scanf("%1d", &bit);
    value = value * 2 + bit;
    read_count = read_count + scanf("%1d", &bit);
    value = value * 2 + bit;
    read_count = read_count + scanf("%1d", &bit);
    value = value * 2 + bit;

    printf("scanf leyó %d dígitos\n", read_count);
    printf("decimal: %d\n", value);
    printf("hexadecimal: %x\n", value);
    return 0;
}
