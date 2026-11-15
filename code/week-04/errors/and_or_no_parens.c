#include <stdio.h>

// Funciona, pero se lee mal: && se agrupa antes que ||.
int main(void) {
    int a = 1;
    int b = 0;
    int c = 1;

    printf("%d\n", a && b || c);

    return 0;
}
