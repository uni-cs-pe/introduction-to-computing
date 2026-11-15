// Los tipos sin signo sí dan la vuelta: C lo define así.
#include <stdio.h>

int main(void) {
    unsigned char b = 255;
    printf("b = %d\n", b);
    b = b + 1;
    printf("b = %d\n", b);
    return 0;
}
