// Lee un byte. Si vale 128 o más, char lo muestra distinto según la plataforma.
#include <limits.h>
#include <stdio.h>

int main(void) {
    char c = 0;
    int read_count = scanf("%c", &c);
    printf("scanf leyó %d dato(s)\n", read_count);

    printf("CHAR_MIN = %d, CHAR_MAX = %d\n", CHAR_MIN, CHAR_MAX);
    printf("como char:          %d\n", c);
    printf("como unsigned char: %d\n", (unsigned char) c);
    return 0;
}
