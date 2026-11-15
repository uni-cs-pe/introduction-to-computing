// Un mismo número, escrito en decimal y en hexadecimal.
#include <stdio.h>

int main(void) {
    int n = 202;
    int m = 0xCA;  // 0x indica que el literal está en hexadecimal

    printf("%d en decimal\n", n);
    printf("%x en hexadecimal, con minúsculas\n", n);
    printf("%X en hexadecimal, con mayúsculas\n", n);
    printf("0xCA vale %d\n", m);
    return 0;
}
